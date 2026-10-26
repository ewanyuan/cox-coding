#!/usr/bin/env python3
"""Record one task at a time and revert it without rewriting history.

The script, not the AI, records the starting commit and creates the commit
when a task finishes. The dashboard computes changed files from git.
Nothing here rejects a commit or installs a hook. Unplanned work is only
reported. Revert uses ``git revert`` (a new commit). A trial revert runs
in a temporary worktree first; conflicts stop the operation and name the
later task that touched the same files.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


AUTHOR_NAME = "COX"
AUTHOR_EMAIL = "cox@localhost"

CHANGE_LABELS = {
    "modified": ("修改", "changed"),
    "added": ("新增", "added"),
    "deleted": ("删除", "deleted"),
    "renamed": ("重命名", "renamed"),
    "copied": ("复制", "copied"),
}


class TrackError(Exception):
    def __init__(self, code, message_zh, message_en, **extra):
        super().__init__(message_zh)
        self.code = code
        self.message_zh = message_zh
        self.message_en = message_en
        self.extra = extra


def ok(code, message_zh, message_en, **extra):
    payload = {"ok": True, "code": code, "message_zh": message_zh, "message_en": message_en}
    payload.update(extra)
    return payload


def fail(code, message_zh, message_en, **extra):
    payload = {"ok": False, "code": code, "message_zh": message_zh, "message_en": message_en}
    payload.update(extra)
    return payload


def _git_env():
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = AUTHOR_NAME
    env["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
    env["GIT_COMMITTER_NAME"] = AUTHOR_NAME
    env["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def run_git(repo, *args, check=True, config=None):
    cmd = ["git"]
    for key, value in (config or {}).items():
        cmd.extend(["-c", f"{key}={value}"])
    cmd.extend(["-C", str(repo)])
    cmd.extend(args)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=_git_env(),
        )
    except FileNotFoundError as exc:
        raise TrackError(
            "no_git",
            "这台电脑上没有找到 Git，所以还不能记录或撤回改动。",
            "Git is not installed, so changes cannot be recorded or reverted.",
        ) from exc
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise TrackError(
            "git_error",
            f"Git 没有完成这一步。项目没有被改掉。原因：{detail}",
            f"Git did not finish this step. The project was left unchanged. Reason: {detail}",
        )
    return result


def find_repo(start):
    start = Path(start).resolve()
    if not start.exists():
        return None
    probe = start if start.is_dir() else start.parent
    result = run_git(probe, "rev-parse", "--show-toplevel", check=False)
    if result.returncode != 0:
        return None
    toplevel = Path(result.stdout.strip()).resolve()
    try:
        probe.relative_to(toplevel)
    except ValueError:
        return None
    return toplevel


def target_dir(project_file, repo_hint=None):
    if repo_hint:
        return Path(repo_hint).resolve()
    return Path(project_file).resolve().parent


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def iter_tasks(project):
    for iteration in project.get("iterations") or []:
        for task in iteration.get("tasks") or []:
            yield iteration, task


def find_task(project, task_id):
    for iteration, task in iter_tasks(project):
        if task.get("task_id") == task_id:
            return iteration, task
    return None, None


def in_progress_tasks(project):
    found = []
    for _iteration, task in iter_tasks(project):
        if task.get("status") == "in_progress":
            found.append(task)
    return found


def tracked_bookkeeping(repo, project_file, app_file=None, test_file=None):
    return bookkeeping_paths(repo, [project_file, app_file, test_file])


def bookkeeping_paths(repo, paths):
    repo = Path(repo).resolve()
    relative = []
    for raw in paths:
        if not raw:
            continue
        path = Path(raw).resolve()
        try:
            rel = path.relative_to(repo).as_posix()
        except ValueError:
            continue
        if rel and rel != ".":
            relative.append(rel)
    return relative


def _split_z(blob):
    parts = blob.split("\0")
    if parts and parts[-1] == "":
        parts.pop()
    return parts


def parse_status_z(blob):
    parts = _split_z(blob)
    entries = []
    index = 0
    while index < len(parts):
        record = parts[index]
        index += 1
        if len(record) < 3:
            continue
        xy = record[:2]
        path = record[3:]
        previous = None
        if "R" in xy or "C" in xy:
            previous = path
            if index >= len(parts):
                break
            path = parts[index]
            index += 1
        entries.append({
            "xy": xy,
            "path": path.replace("\\", "/"),
            "previous": previous.replace("\\", "/") if previous else None,
        })
    return entries


def parse_name_status_z(blob):
    parts = _split_z(blob)
    entries = []
    index = 0
    while index < len(parts):
        status = parts[index]
        index += 1
        if not status:
            continue
        code = status[0]
        if code in "RC":
            if index + 1 >= len(parts):
                break
            previous = parts[index].replace("\\", "/")
            path = parts[index + 1].replace("\\", "/")
            index += 2
            kind = "renamed" if code == "R" else "copied"
            entries.append({"change": kind, "path": path, "previous": previous})
            continue
        if index >= len(parts):
            break
        path = parts[index].replace("\\", "/")
        index += 1
        kind = {
            "M": "modified",
            "A": "added",
            "D": "deleted",
            "T": "modified",
            "U": "modified",
        }.get(code, "modified")
        entries.append({"change": kind, "path": path, "previous": None})
    return entries


def _decorate(entry):
    zh, en = CHANGE_LABELS.get(entry["change"], ("修改", "changed"))
    decorated = dict(entry)
    decorated["label_zh"] = zh
    decorated["label_en"] = en
    return decorated


def worktree_entries(repo):
    result = run_git(repo, "status", "--porcelain=v1", "-z", "-uall", check=False)
    if result.returncode != 0:
        return []
    return parse_status_z(result.stdout)


def user_dirty_paths(repo, ignored):
    ignored = set(ignored)
    dirty = []
    for entry in worktree_entries(repo):
        if entry["path"] in ignored:
            continue
        if entry["previous"] and entry["previous"] in ignored and entry["path"] in ignored:
            continue
        dirty.append(entry["path"])
    return dirty


def _commit(repo, message, trailers, allow_empty=False):
    args = ["commit", "-m", message]
    for key, value in trailers:
        args.extend(["-m", f"{key}: {value}"])
    if allow_empty:
        args.append("--allow-empty")
    run_git(repo, *args, config={"commit.gpgsign": "false"})
    return run_git(repo, "rev-parse", "HEAD").stdout.strip()


def _meta_commit_bookkeeping(repo, relative_paths):
    existing = [rel for rel in relative_paths if (Path(repo) / rel).exists()]
    if not existing:
        return None
    run_git(repo, "add", "--", *existing, check=False)
    staged = run_git(repo, "diff", "--cached", "--quiet", check=False)
    if staged.returncode == 0:
        return None
    return _commit(repo, "cox: record task state", [("Cox-Meta", "true")])


def _stage_task_changes(repo, ignored):
    run_git(repo, "add", "-A")
    for rel in ignored:
        run_git(repo, "reset", "HEAD", "--", rel, check=False)
    staged = run_git(repo, "diff", "--cached", "--name-only", "-z")
    names = [part for part in _split_z(staged.stdout) if part]
    return names


def diff_between(repo, start, end):
    if not start or not end or start == end:
        return []
    result = run_git(repo, "diff", "--name-status", "-z", start, end, check=False)
    if result.returncode != 0:
        return []
    return [_decorate(item) for item in parse_name_status_z(result.stdout)]


def diff_worktree(repo, start, ignored):
    ignored = set(ignored)
    combined = []
    if start:
        result = run_git(repo, "diff", "--name-status", "-z", start, check=False)
        if result.returncode == 0:
            combined.extend(parse_name_status_z(result.stdout))
        staged = run_git(repo, "diff", "--cached", "--name-status", "-z", check=False)
        if staged.returncode == 0:
            combined.extend(parse_name_status_z(staged.stdout))
    others = run_git(repo, "ls-files", "--others", "--exclude-standard", "-z", check=False)
    if others.returncode == 0:
        for part in _split_z(others.stdout):
            combined.append({"change": "added", "path": part.replace("\\", "/"), "previous": None})
    deduped = {}
    for item in combined:
        if item["path"] in ignored:
            continue
        deduped[item["path"]] = item
    return [_decorate(item) for item in deduped.values()]


def _module_index(project, app):
    by_id = {}
    for iteration in project.get("iterations") or []:
        for module in iteration.get("modules") or []:
            module_id = module.get("module_id")
            if module_id:
                by_id[module_id] = module.get("module_name") or module_id
    for module in (app or {}).get("modules") or []:
        module_id = module.get("module_id")
        if module_id and module_id not in by_id:
            by_id[module_id] = module.get("module_name") or module_id
    return by_id


def _belongs(task, names):
    found = []
    for module_id in task.get("module_ids") or []:
        if not isinstance(module_id, str):
            continue
        found.append({"module_id": module_id, "module_name": names.get(module_id, module_id)})
    return found


def _history(repo):
    result = run_git(repo, "rev-list", "--first-parent", "--reverse", "HEAD", check=False)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _log_records(repo):
    result = run_git(repo, "log", "--first-parent", "--format=%H%x1f%B%x1e", "HEAD", check=False)
    if result.returncode != 0:
        return []
    records = []
    for chunk in result.stdout.split("\x1e"):
        chunk = chunk.strip("\n")
        if not chunk.strip():
            continue
        sha, _sep, body = chunk.partition("\x1f")
        sha = sha.strip()
        if len(sha) < 7:
            continue
        records.append({"sha": sha, "body": body})
    return records


def _subject(body):
    for line in body.splitlines():
        if line.strip():
            return line.strip()
    return ""


def _has_trailer(body, key):
    prefix = key + ":"
    for line in body.splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""


def commit_files(repo, sha):
    result = run_git(repo, "diff-tree", "--no-commit-id", "--name-status", "-r", "-z", sha, check=False)
    if result.returncode != 0:
        return []
    root = run_git(repo, "rev-parse", "--verify", sha + "^", check=False)
    if root.returncode != 0:
        show = run_git(repo, "diff-tree", "--root", "--no-commit-id", "--name-status", "-r", "-z", sha, check=False)
        result = show
    return [_decorate(item) for item in parse_name_status_z(result.stdout)]


def _file_set(files):
    names = set()
    for item in files:
        names.add(item["path"])
        if item.get("previous"):
            names.add(item["previous"])
    return names


def _task_files(repo, task, ignored):
    start = task.get("start_commit")
    end = task.get("end_commit")
    if task.get("status") == "in_progress" and start:
        return diff_worktree(repo, start, ignored)
    if start and end:
        return [item for item in diff_between(repo, start, end) if item["path"] not in ignored]
    return []


def _unattributed(repo, project):
    owned = set()
    for _iteration, task in iter_tasks(project):
        for key in ("end_commit", "revert_commit", "start_commit"):
            value = task.get(key)
            if isinstance(value, str) and value:
                owned.add(value)
    records = _log_records(repo)
    reverted = set()
    for record in records:
        value = _has_trailer(record["body"], "This-Reverts-Commit")
        if value:
            reverted.add(value.strip())
    found = []
    for record in records:
        sha = record["sha"]
        body = record["body"]
        if sha in owned or sha in reverted:
            continue
        if _has_trailer(body, "Cox-Meta") or _has_trailer(body, "Cox-Init") or _has_trailer(body, "Cox-Revert"):
            continue
        files = commit_files(repo, sha)
        found.append({
            "commit": sha,
            "subject": _subject(body) or sha[:7],
            "files": files,
            "attribution": "unattributed",
        })
    return found


def build_observation(project_file, app_file=None, repo=None, test_file=None):
    project = load_json(project_file)
    app = load_json(app_file) if app_file and Path(app_file).exists() else {"modules": []}
    directory = target_dir(project_file, repo)
    git_root = find_repo(directory)
    names = _module_index(project, app)
    base = {
        "git_repo": git_root is not None,
        "repo": str(git_root) if git_root else None,
        "revert_available": git_root is not None,
        "init_available": git_root is None,
        "tasks": {},
        "unattributed": [],
        "message_zh": "",
        "message_en": "",
    }
    if git_root is None:
        base["revert_available"] = False
        base["message_zh"] = (
            "这个项目还没有版本记录，所以看不到实际改了哪些文件，也不能撤回。"
            "只有你同意之后，才会在项目里开始用 Git 记录版本。"
        )
        base["message_en"] = (
            "This project has no version history, so the files actually changed cannot be listed and revert is hidden. "
            "Git is started only after you agree."
        )
    ignored = tracked_bookkeeping(git_root, project_file, app_file, test_file) if git_root else []
    ignored_set = set(ignored)
    order = _history(git_root) if git_root else []
    position = {sha: index for index, sha in enumerate(order)}
    file_cache = {}

    def files_for(task):
        task_id = task.get("task_id")
        if task_id not in file_cache:
            file_cache[task_id] = _task_files(git_root, task, ignored_set) if git_root else []
        return file_cache[task_id]

    if git_root:
        base["unattributed"] = _unattributed(git_root, project)

    shared = {}
    if git_root:
        for _iteration, task in iter_tasks(project):
            end = task.get("end_commit")
            if isinstance(end, str) and end and end != task.get("start_commit"):
                shared.setdefault(end, []).append(task)

    for iteration, task in iter_tasks(project):
        task_id = task.get("task_id")
        if not task_id:
            continue
        belongs = _belongs(task, names)
        planned = []
        planned_ids = set()
        for module in iteration.get("modules") or []:
            module_id = module.get("module_id")
            module_name = module.get("module_name") or module_id
            if module_id:
                planned_ids.add(module_id)
            planned.append({"module_id": module_id, "module_name": module_name})
        unplanned_modules = [item for item in belongs if item["module_id"] not in planned_ids]
        missing_link = not belongs
        files = files_for(task) if git_root else []
        end = task.get("end_commit")
        partners = []
        if end and end in shared and len(shared[end]) > 1:
            partners = [
                {"task_id": other.get("task_id"), "task_name": other.get("task_name") or other.get("task_id")}
                for other in shared[end]
            ]
        later = []
        if git_root and end and end in position:
            mine = _file_set(files)
            for other_iteration, other in iter_tasks(project):
                if other.get("task_id") == task_id or other.get("status") == "reverted":
                    continue
                other_end = other.get("end_commit")
                if not other_end or other_end not in position or position[other_end] <= position[end]:
                    continue
                if mine & _file_set(files_for(other)):
                    later.append({
                        "task_id": other.get("task_id"),
                        "task_name": other.get("task_name") or other.get("task_id"),
                    })
        notice_zh = ""
        notice_en = ""
        if unplanned_modules:
            listed = "、".join(f"「{item['module_name']}」" for item in unplanned_modules)
            listed_en = ", ".join(item["module_name"] for item in unplanned_modules)
            notice_zh = (
                f"计划外：这次任务属于{listed}，这轮计划里没有"
                f"{'它' if len(unplanned_modules) == 1 else '这些功能'}。"
                "这只是提醒，不会阻止任何修改。"
            )
            notice_en = (
                f"Unplanned: this task belongs to {listed_en}, which this round did not plan to change. "
                "This is only a notice — nothing is blocked."
            )
        elif missing_link:
            notice_zh = "这次任务还没有写它属于哪个功能。这只是提醒，不会阻止修改。"
            notice_en = "This task is not linked to a feature yet. This is only a notice — nothing is blocked."
        reverted = task.get("status") == "reverted" or bool(task.get("revert_commit"))
        has_code_commit = bool(end) and end != task.get("start_commit") and not reverted
        base["tasks"][task_id] = {
            "task_id": task_id,
            "task_name": task.get("task_name") or task_id,
            "state": "reverted" if reverted else task.get("status") or "todo",
            "changed_files": files,
            "belongs_to": belongs,
            "planned": planned,
            "unplanned": bool(unplanned_modules),
            "missing_link": missing_link,
            "notice_zh": notice_zh,
            "notice_en": notice_en,
            "later_tasks": later,
            "mixed_with": partners,
            "attribution": "mixed" if len(partners) > 1 else ("task" if has_code_commit or task.get("start_commit") else "none"),
            "revertible": bool(git_root and has_code_commit),
            "reverted": reverted,
            "start_commit": task.get("start_commit"),
            "end_commit": end,
        }
    return base


def _require_repo(project_file, repo_hint):
    directory = target_dir(project_file, repo_hint)
    git_root = find_repo(directory)
    if git_root is None:
        raise TrackError(
            "not_git",
            "这个项目还没有版本记录。请先问用户是否同意开始记录；只有用户同意后才能运行 init --agree。不要自行 git init。不同意的话，不要显示撤回。",
            "This project has no version history. Ask the user before running init --agree. Do not run git init on your own. Hide revert if they do not agree.",
            git_repo=False,
            revert_available=False,
        )
    return git_root


def _stash_paths(repo, paths, message):
    if not paths:
        return None
    result = run_git(
        repo,
        "stash",
        "push",
        "--include-untracked",
        "-m",
        message,
        "--",
        *paths,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise TrackError(
            "stash_failed",
            f"没能把你还没保存的修改放一边，所以这一步停了。那些修改还在原地。原因：{detail}",
            f"Could not set your unsaved edits aside, so this step stopped. Those edits are still in place. Reason: {detail}",
        )
    return run_git(repo, "rev-parse", "stash@{0}").stdout.strip()


def _restore_stash(repo, sha):
    if not sha:
        return "none"
    listing = run_git(repo, "stash", "list", "--format=%gd %H", check=False)
    selector = None
    for line in listing.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == sha:
            selector = parts[0]
            break
    if selector is None:
        return "missing"
    applied = run_git(repo, "stash", "apply", selector, check=False)
    if applied.returncode != 0:
        # Abort the failed apply. The stash entry itself is kept.
        run_git(repo, "reset", "--merge", check=False)
        return "conflict"
    run_git(repo, "stash", "drop", selector, check=False)
    return "restored"


def start_task(project_file, task_id, repo=None, adopt=False, stash=False, app_file=None, test_file=None):
    project = load_json(project_file)
    _iteration, task = find_task(project, task_id)
    if task is None:
        return fail("missing_task", f"没有找到任务 {task_id}。", f"Task {task_id} was not found.")
    if task.get("status") == "reverted" or task.get("revert_commit"):
        return fail(
            "already_reverted",
            "这个任务已经撤回过了。请新开一个任务，不要接着用同一个任务号。",
            "This task was already reverted. Start a new task instead of reusing this one.",
        )
    if task.get("end_commit") and task.get("status") != "in_progress":
        return fail(
            "already_finished",
            "这个任务已经记过结束版本了。请新开一个任务。",
            "This task already has an end commit. Start a new task.",
        )
    others = [item for item in in_progress_tasks(project) if item.get("task_id") != task_id]
    if others:
        other = others[0]
        name = other.get("task_name") or other.get("task_id")
        return fail(
            "busy",
            f"现在已经有一个任务在进行：「{name}」。请先结束它，再开始新的。同一时间只能记一个任务，否则分不清改动是谁的。",
            f"A task is already in progress: \"{name}\". Finish it before starting another. Only one task can be in progress at a time.",
            blocking_task=other.get("task_id"),
        )
    try:
        git_root = _require_repo(project_file, repo)
    except TrackError as exc:
        return fail(exc.code, exc.message_zh, exc.message_en, **exc.extra)
    head = run_git(git_root, "rev-parse", "HEAD", check=False)
    if head.returncode != 0:
        return fail(
            "no_snapshot",
            "版本记录里还没有任何一次保存。请先在用户同意后做一次初始记录。",
            "Version history has no snapshot yet. Create the initial snapshot after the user agrees.",
        )
    if task.get("status") == "in_progress" and task.get("start_commit"):
        return ok(
            "already_started",
            "这个任务已经在进行中，开始时的版本没有改。",
            "This task is already in progress; the starting commit was left as recorded.",
            start_commit=task.get("start_commit"),
            task_id=task_id,
        )
    ignored = tracked_bookkeeping(git_root, project_file, app_file, test_file)
    dirty = user_dirty_paths(git_root, ignored)
    if dirty and not adopt and not stash:
        listed = "、".join(dirty[:12])
        return fail(
            "dirty",
            f"还有 {len(dirty)} 个文件改了、还没保存成版本：{listed}。请先问用户这些改动算这次任务（--adopt）还是先放一边（--stash）。不要丢弃它们。",
            f"{len(dirty)} file(s) are edited but not saved as a version: {', '.join(dirty[:12])}. Ask whether they belong to this task (--adopt) or should be set aside (--stash). Do not discard them.",
            dirty_files=dirty,
        )
    paused = None
    if dirty and stash:
        paused = _stash_paths(git_root, dirty, f"cox: set aside unsaved edits before {task_id}")
    head_sha = run_git(git_root, "rev-parse", "HEAD").stdout.strip()
    task["status"] = "in_progress"
    task["start_commit"] = head_sha
    if paused:
        task["paused_user_changes"] = paused
    elif "paused_user_changes" in task and not stash:
        task.pop("paused_user_changes", None)
    save_json(project_file, project)
    return ok(
        "started",
        f"已记下任务「{task.get('task_name') or task_id}」开始时的版本。结束时请运行 finish，不要自己提交。",
        f"Recorded the starting commit for \"{task.get('task_name') or task_id}\". Run finish at the end; do not commit the task yourself.",
        start_commit=head_sha,
        task_id=task_id,
        stashed=bool(paused),
    )


def finish_task(project_file, task_id, repo=None, app_file=None, test_file=None):
    project = load_json(project_file)
    _iteration, task = find_task(project, task_id)
    if task is None:
        return fail("missing_task", f"没有找到任务 {task_id}。", f"Task {task_id} was not found.")
    if task.get("status") != "in_progress":
        if task.get("end_commit"):
            return ok(
                "already_finished",
                "这个任务已经结束，没有再提交一次。",
                "This task is already finished; nothing new was committed.",
                end_commit=task.get("end_commit"),
                task_id=task_id,
            )
        return fail(
            "not_started",
            "还没有开始记录这个任务，所以没有替你提交。请先运行 start。",
            "This task was not started, so nothing was committed. Run start first.",
        )
    try:
        git_root = _require_repo(project_file, repo)
    except TrackError as exc:
        return fail(exc.code, exc.message_zh, exc.message_en, **exc.extra)
    ignored = tracked_bookkeeping(git_root, project_file, app_file, test_file)
    paused = task.get("paused_user_changes")
    try:
        staged_names = _stage_task_changes(git_root, ignored)
        start = task.get("start_commit")
        if staged_names:
            name = (task.get("task_name") or task_id).replace("\n", " ").strip()
            end = _commit(
                git_root,
                f"cox: {task_id} {name}",
                [("Cox-Task", task_id)],
            )
        else:
            end = start
        task["status"] = "done"
        task["end_commit"] = end
        save_json(project_file, project)
        _meta_commit_bookkeeping(git_root, tracked_bookkeeping(git_root, project_file, app_file, test_file))
        restore_note = ""
        if paused:
            restored = _restore_stash(git_root, paused)
            if restored == "restored":
                task.pop("paused_user_changes", None)
                save_json(project_file, project)
                _meta_commit_bookkeeping(git_root, tracked_bookkeeping(git_root, project_file, app_file, test_file))
                restore_note = "开工前放一边的修改已经放回来了。"
            elif restored == "conflict":
                restore_note = "任务已经记完。开工前放一边的修改还在暂存里，没有丢掉，但放回来时对不上，需要让 AI 看一下。"
            else:
                restore_note = "任务已经记完。没有找到开工前放一边的修改。"
        files = diff_between(git_root, start, end)
        files = [item for item in files if item["path"] not in set(ignored)]
        message_zh = f"已把任务「{task.get('task_name') or task_id}」的改动记成一个版本。{restore_note}"
        message_en = f"Recorded one commit for \"{task.get('task_name') or task_id}\". {restore_note}"
        return ok(
            "finished",
            message_zh,
            message_en,
            task_id=task_id,
            start_commit=start,
            end_commit=end,
            changed_files=files,
        )
    except Exception:
        if paused:
            _restore_stash(git_root, paused)
        raise


def _person_name(item, lang):
    if str(item.get("task_id", "")).startswith("unattributed:"):
        return "未归属改动" if lang == "zh" else "unattributed changes"
    if lang == "en":
        return item.get("task_name_en") or item.get("task_name") or item.get("task_id")
    return item.get("task_name") or item.get("task_id")


def _revert_paragraphs(title_names, files, later, conflict, dirty, mixed, unattributed=False):
    file_zh = _join_files(files, "zh")
    file_en = _join_files(files, "en")
    names_zh = "、".join(f"「{name}」" for name in title_names)
    names_en = ", ".join(f"\"{name}\"" for name in title_names)
    later_zh = "、".join(f"「{_person_name(item, 'zh')}」" for item in later)
    later_en = ", ".join(f"\"{_person_name(item, 'en')}\"" for item in later)
    limit_zh = "请注意：数据库里的改动、已经安装的依赖、以及已经发布出去的内容，都不能撤回。如果这些代码曾经同步到网上，撤回之后还需要再同步一次。"
    limit_en = "Database changes, installed dependencies, and anything already published cannot be reverted. If this code was already synced to the network, it needs to be synced again after a revert."
    zh = []
    en = []
    if unattributed:
        zh.append("这些改动没有归到单独的任务，标成「未归属改动」。只能整次一起撤回，不能拆开。")
        en.append("These edits are not tied to one task. They are labeled unattributed changes and can only be reverted together.")
    if mixed and len(title_names) > 1:
        zh.append(f"这次提交同时包含{names_zh}，只能一起撤回。")
        en.append(f"This commit mixed {names_en} and can only be reverted together.")
    if conflict:
        who = later_zh or "后来的未归属改动"
        who_en = later_en or "a later unattributed change"
        zh.append(f"现在还不能撤回{names_zh}。后来的任务{who}也改了同样的文件，直接撤回会对不上。已经停下来了，没有改你的项目，也不会自动合并。")
        zh.append("可以先撤回后来的那一次，或者让 AI 手动处理。")
        en.append(f"Cannot revert {names_en} yet. Later work ({who_en}) also changed the same files, so a revert would conflict. It stopped. Your project was not changed, and conflicts are never resolved automatically.")
        en.append("Revert the later task first, or ask the AI to handle it by hand.")
        zh.append(limit_zh)
        en.append(limit_en)
        return {"zh": zh, "en": en}
    zh.append(f"要撤回{names_zh}吗？")
    en.append(f"Revert {names_en}?")
    zh.append("这一步只会把这次改过的代码文件改回去，并在记录里多留一条「改回去」的版本。以前的记录都还在，不会删掉历史。")
    en.append("This only puts the code files from this task back, by adding a new \"put it back\" commit. Earlier history stays. Nothing is erased.")
    zh.append(f"这次实际改过的文件：{file_zh}。")
    en.append(f"Files actually changed: {file_en}.")
    zh.append(limit_zh)
    en.append(limit_en)
    if later and not conflict:
        zh.append(f"后来的任务{later_zh}也改过其中的文件。这次试撤回没有冲突，但撤回后请再看一眼那些功能是否还正常。")
        en.append(f"Later task(s) {later_en} also touched some of these files. The trial revert did not conflict, but please check those features again afterwards.")
    if dirty:
        zh.append(f"你还有 {len(dirty)} 个文件改了、还没保存成版本：{'、'.join(dirty[:12])}。这些不会丢掉。可以先放一边，撤回完成后再放回来；也可以先不撤回。")
        en.append(f"You still have {len(dirty)} unsaved file(s): {', '.join(dirty[:12])}. They will not be discarded. They can be set aside and put back after the revert, or you can cancel.")
    return {"zh": zh, "en": en}


def _join_files(files, lang):
    if not files:
        return "没有改到代码文件" if lang == "zh" else "no code files"
    parts = []
    for item in files[:30]:
        if lang == "zh":
            parts.append(f"{item['path']}（{item['label_zh']}）")
        else:
            parts.append(f"{item['path']} ({item['label_en']})")
    if len(files) > 30:
        extra = len(files) - 30
        parts.append(f"等 {extra} 个" if lang == "zh" else f"and {extra} more")
    return "、".join(parts) if lang == "zh" else ", ".join(parts)


def _resolve_revert_target(project, repo, task_id):
    if task_id.startswith("unattributed:"):
        sha = task_id.split(":", 1)[1].strip()
        known = {item["commit"] for item in _unattributed(repo, project)}
        if sha not in known:
            raise TrackError(
                "not_unattributed",
                "这次提交不能单独按这个请求撤回。它要么已经归到任务，要么不是当前版本线上的未归属改动。",
                "That commit cannot be reverted this way. It is either already tied to a task, or it is not an unattributed commit on the current history.",
            )
        parents = run_git(repo, "rev-parse", "--verify", sha + "^2", check=False)
        if parents.returncode == 0:
            raise TrackError(
                "merge_commit",
                "这次提交是一次合并，不能自动撤回。请让 AI 手动处理。项目没有被改。",
                "That commit is a merge and cannot be reverted automatically. Ask the AI to handle it. The project was not changed.",
            )
        return {
            "commit": sha,
            "tasks": [],
            "unattributed": True,
            "names": ["未归属改动" if True else ""],
        }
    _iteration, task = find_task(project, task_id)
    if task is None:
        raise TrackError("missing_task", f"没有找到任务 {task_id}。", f"Task {task_id} was not found.")
    if task.get("status") == "reverted" or task.get("revert_commit"):
        raise TrackError(
            "already_reverted",
            "这个任务已经撤回过了，记录还在。",
            "This task was already reverted. The history is still there.",
        )
    end = task.get("end_commit")
    start = task.get("start_commit")
    if not end or end == start:
        raise TrackError(
            "no_commit",
            "这次任务没有单独的代码版本，所以没有东西可撤回。",
            "This task has no code commit of its own, so there is nothing to revert.",
        )
    group = []
    for _it, other in iter_tasks(project):
        if other.get("end_commit") == end and other.get("status") != "reverted" and not other.get("revert_commit"):
            group.append(other)
    if not group:
        group = [task]
    return {
        "commit": end,
        "tasks": group,
        "unattributed": False,
        "names": [item.get("task_name") or item.get("task_id") for item in group],
    }


def _later_overlap(project, repo, commit, ignored):
    order = _history(repo)
    position = {sha: index for index, sha in enumerate(order)}
    if commit not in position:
        return []
    mine = _file_set(commit_files(repo, commit))
    later = []
    for _iteration, other in iter_tasks(project):
        other_end = other.get("end_commit")
        if not other_end or other_end == commit:
            continue
        if other.get("status") == "reverted" or other.get("revert_commit"):
            continue
        if other_end not in position or position[other_end] <= position[commit]:
            continue
        other_files = [item for item in diff_between(repo, other.get("start_commit"), other_end) if item["path"] not in ignored]
        if mine & _file_set(other_files):
            later.append({
                "task_id": other.get("task_id"),
                "task_name": other.get("task_name") or other.get("task_id"),
                "task_name_en": other.get("task_name") or other.get("task_id"),
            })
    if not later:
        for item in _unattributed(repo, project):
            if item["commit"] not in position or position[item["commit"]] <= position[commit]:
                continue
            if mine & _file_set(item["files"]):
                later.append({
                    "task_id": "unattributed:" + item["commit"],
                    "task_name": "未归属改动",
                    "task_name_en": "unattributed changes",
                })
                break
    return later


def try_revert_in_worktree(repo, commit):
    """Return (clean, detail). The user's worktree is not modified."""
    temporary = Path(tempfile.mkdtemp(prefix="cox-revert-try-"))
    try:
        added = run_git(repo, "worktree", "add", "--detach", str(temporary), "HEAD", check=False)
        if added.returncode != 0:
            detail = (added.stderr or added.stdout or "").strip()
            return False, f"无法先试撤回。项目没有被改。原因：{detail}"
        trial = run_git(temporary, "revert", "--no-commit", commit, check=False)
        output = ((trial.stdout or "") + "\n" + (trial.stderr or "")).strip()
        unmerged = run_git(temporary, "diff", "--name-only", "--diff-filter=U", check=False)
        conflicted = trial.returncode != 0 or bool(unmerged.stdout.strip()) or "CONFLICT" in output
        if conflicted:
            run_git(temporary, "revert", "--abort", check=False)
            return False, output
        return True, output
    finally:
        run_git(repo, "worktree", "remove", "--force", str(temporary), check=False)
        shutil.rmtree(temporary, ignore_errors=True)
        run_git(repo, "worktree", "prune", check=False)


def preview_revert(project_file, task_id, repo=None, app_file=None, test_file=None):
    try:
        project = load_json(project_file)
        git_root = _require_repo(project_file, repo)
        target = _resolve_revert_target(project, git_root, task_id)
    except TrackError as exc:
        paragraphs = {"zh": [exc.message_zh], "en": [exc.message_en]}
        if exc.code != "not_git":
            paragraphs["zh"].append("请注意：数据库里的改动、已经安装的依赖、以及已经发布出去的内容，都不能撤回。")
            paragraphs["en"].append("Database changes, installed dependencies, and anything already published cannot be reverted.")
        return fail(exc.code, exc.message_zh, exc.message_en, can_revert=False, conflict=False, paragraphs=paragraphs, **exc.extra)
    commit = target["commit"]
    ancestor = run_git(git_root, "merge-base", "--is-ancestor", commit, "HEAD", check=False)
    if ancestor.returncode != 0:
        message_zh = "这次修改不在当前的版本线上，没有撤回，项目保持原样。"
        message_en = "That change is not on the current history. Nothing was reverted."
        return fail("not_ancestor", message_zh, message_en, can_revert=False, conflict=False, paragraphs={"zh": [message_zh], "en": [message_en]})
    ignored = set(tracked_bookkeeping(git_root, project_file, app_file, test_file))
    files = [item for item in commit_files(git_root, commit) if item["path"] not in ignored]
    later = _later_overlap(project, git_root, commit, ignored)
    clean, detail = try_revert_in_worktree(git_root, commit)
    dirty = user_dirty_paths(git_root, ignored)
    mixed = len(target["tasks"]) > 1
    paragraphs = _revert_paragraphs(target["names"], files, later, conflict=not clean, dirty=dirty, mixed=mixed, unattributed=target["unattributed"])
    if not clean:
        return ok(
            "conflict",
            paragraphs["zh"][0],
            paragraphs["en"][0],
            can_revert=False,
            conflict=True,
            needs_stash=False,
            dirty_files=dirty,
            later_tasks=later,
            files=files,
            together=[{"task_id": item.get("task_id"), "task_name": item.get("task_name")} for item in target["tasks"]],
            paragraphs=paragraphs,
            commit=commit,
            detail=detail,
        )
    return ok(
        "ready" if not dirty else "dirty",
        paragraphs["zh"][0],
        paragraphs["en"][0],
        can_revert=not dirty,
        needs_stash=bool(dirty),
        conflict=False,
        dirty_files=dirty,
        later_tasks=later,
        files=files,
        together=[{"task_id": item.get("task_id"), "task_name": item.get("task_name")} for item in target["tasks"]],
        paragraphs=paragraphs,
        commit=commit,
        unattributed=target["unattributed"],
    )


def _mark_reverted(project, app, tasks, revert_sha):
    note_ids = []
    for task in tasks:
        task["status"] = "reverted"
        task["revert_commit"] = revert_sha
        for module_id in task.get("module_ids") or []:
            note_ids.append((module_id, task.get("task_name") or task.get("task_id")))
    if not app:
        return
    names = {}
    for iteration, _task in iter_tasks(project):
        for module in iteration.get("modules") or []:
            if module.get("module_id"):
                names[module["module_id"]] = module.get("module_name")
    for module_id, task_name in note_ids:
        module_name = names.get(module_id)
        for module in app.get("modules") or []:
            matched = module.get("module_id") == module_id or (module_name and module.get("module_name") == module_name)
            if not matched:
                continue
            if module.get("status") == "optimized":
                module["status"] = "confirmed"
            extra = f"任务「{task_name}」已撤回，请再看一眼这个功能。"
            notes = module.get("notes") or ""
            if extra not in notes:
                module["notes"] = (notes + " " + extra).strip()


def execute_revert(project_file, task_id, repo=None, app_file=None, test_file=None, confirm=False, stash=False):
    if not confirm:
        return fail(
            "need_confirm",
            "还没有确认，没有撤回。",
            "Not confirmed, so nothing was reverted.",
            can_revert=False,
        )
    preview = preview_revert(project_file, task_id, repo=repo, app_file=app_file, test_file=test_file)
    if preview.get("conflict") or preview.get("code") in {"not_git", "missing_task", "already_reverted", "no_commit", "not_ancestor", "merge_commit", "not_unattributed"}:
        preview["ok"] = False
        if preview.get("conflict"):
            preview["code"] = "conflict"
            preview["ok"] = False
        return preview
    if not preview.get("ok"):
        return preview
    if preview.get("needs_stash") and not stash:
        preview["ok"] = False
        preview["code"] = "dirty"
        preview["can_revert"] = False
        return preview
    project = load_json(project_file)
    app = load_json(app_file) if app_file and Path(app_file).exists() else None
    git_root = _require_repo(project_file, repo)
    ignored = tracked_bookkeeping(git_root, project_file, app_file, test_file)
    dirty = user_dirty_paths(git_root, ignored)
    paused = None
    if dirty:
        if not stash:
            return fail(
                "dirty",
                "你还有修改没保存成版本，所以没有撤回。那些修改还在原地。",
                "There are unsaved edits, so nothing was reverted. Those edits are still in place.",
                dirty_files=dirty,
                can_revert=False,
            )
        paused = _stash_paths(git_root, dirty, "cox: set aside unsaved edits before revert")
    commit = preview["commit"]
    clean, detail = try_revert_in_worktree(git_root, commit)
    if not clean:
        if paused:
            _restore_stash(git_root, paused)
        later = preview.get("later_tasks") or []
        names = "、".join(item["task_name"] for item in later) or "后来的改动"
        return fail(
            "conflict",
            f"试撤回时对不上，已经停下来。后来的任务改过同样的文件：{names}。没有自动合并，你的未保存修改也还在。",
            f"The trial revert conflicted, so it stopped. Later work touched the same files: {names}. Conflicts were not resolved, and unsaved edits are still there.",
            conflict=True,
            can_revert=False,
            later_tasks=later,
            detail=detail,
        )
    before = run_git(git_root, "rev-parse", "HEAD").stdout.strip()
    try:
        trial = run_git(git_root, "revert", "--no-commit", commit, check=False)
        output = ((trial.stdout or "") + "\n" + (trial.stderr or "")).strip()
        unmerged = run_git(git_root, "diff", "--name-only", "--diff-filter=U", check=False)
        if trial.returncode != 0 or unmerged.stdout.strip() or "CONFLICT" in output:
            run_git(git_root, "revert", "--abort", check=False)
            raise TrackError(
                "conflict",
                "撤回对不上，已经停下来并恢复原样。没有自动合并。",
                "The revert conflicted, stopped, and put the project back. Conflicts were not resolved.",
            )
        label = "、".join(preview.get("paragraphs", {}).get("zh", [])[:1]) or task_id
        names = " + ".join(item.get("task_name") or item.get("task_id") for item in (preview.get("together") or [])) or task_id
        revert_sha = _commit(
            git_root,
            f"cox: revert {names}",
            [("Cox-Revert", task_id), ("This-Reverts-Commit", commit)],
        )
        if revert_sha == before:
            raise TrackError("revert_failed", "没有产生撤回记录，项目保持原样。", "No revert commit was created. The project was left unchanged.")
        target_tasks = []
        if task_id.startswith("unattributed:"):
            target_tasks = []
        else:
            end = commit
            for _it, other in iter_tasks(project):
                if other.get("end_commit") == end:
                    target_tasks.append(other)
        _mark_reverted(project, app, target_tasks, revert_sha)
        save_json(project_file, project)
        if app is not None and app_file:
            from datetime import datetime
            app["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_json(app_file, app)
        _meta_commit_bookkeeping(git_root, tracked_bookkeeping(git_root, project_file, app_file, test_file))
        restore_note_zh = ""
        restore_note_en = ""
        if paused:
            restored = _restore_stash(git_root, paused)
            if restored == "restored":
                restore_note_zh = "你之前没保存的修改已经放回来了。"
                restore_note_en = "Your unsaved edits were put back."
            else:
                restore_note_zh = "撤回已经完成。你之前没保存的修改还在暂存里，没有丢掉。"
                restore_note_en = "The revert is done. Your unsaved edits are still in the stash and were not discarded."
        return ok(
            "reverted",
            f"已经撤回，并保留了原来的记录。{restore_note_zh}数据库里的改动、已经安装的依赖和已经发布的内容并没有撤回。",
            f"Reverted, and the earlier history is still there. {restore_note_en} Database changes, installed dependencies, and anything already published were not reverted.",
            revert_commit=revert_sha,
            commit=commit,
            task_id=task_id,
            can_revert=False,
        )
    except Exception:
        run_git(git_root, "revert", "--abort", check=False)
        if paused:
            _restore_stash(git_root, paused)
        if isinstance(exc := sys.exc_info()[1], TrackError):
            return fail(exc.code, exc.message_zh, exc.message_en, can_revert=False, conflict=exc.code == "conflict")
        raise


def init_repository(directory, agree):
    directory = Path(directory).resolve()
    if not agree:
        return fail(
            "need_agreement",
            "还没有开始记录版本。需要你同意之后才会创建 Git 仓库。不同意的话，这里不提供撤回。",
            "Version history has not been started. A Git repository is created only after you agree. Otherwise revert stays hidden.",
            git_repo=False,
            revert_available=False,
        )
    existing = find_repo(directory)
    if existing:
        return ok(
            "already",
            "这个项目已经有版本记录，没有重复创建。",
            "This project already has version history. A second repository was not created.",
            git_repo=True,
            repo=str(existing),
            revert_available=True,
        )
    directory.mkdir(parents=True, exist_ok=True)
    run_git(directory, "init", "-b", "main")
    run_git(directory, "add", "-A")
    staged = run_git(directory, "diff", "--cached", "--quiet", check=False)
    if staged.returncode == 0:
        sha = _commit(directory, "cox: initial snapshot", [("Cox-Init", "true")], allow_empty=True)
    else:
        sha = _commit(directory, "cox: initial snapshot", [("Cox-Init", "true")])
    return ok(
        "initialized",
        "已经按你的同意开始记录版本，并保存了当前文件作为起点。撤回只针对这之后的代码改动。",
        "Version history has started with your agreement, and the current files were saved as the starting point. Revert applies only to code changes after this.",
        git_repo=True,
        repo=str(directory),
        revert_available=True,
        commit=sha,
    )


def _print_payload(payload, as_json, lang):
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload.get("message_en") if lang == "en" else payload.get("message_zh"))
    return 0 if payload.get("ok") else 2


def main(argv=None):
    parser = argparse.ArgumentParser(description="记录任务的开始和结束，并安全撤回一次任务的代码改动。")
    parser.add_argument("--json", action="store_true", help="用 JSON 输出结果")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    sub = parser.add_subparsers(dest="command")

    start = sub.add_parser("start", help="记下任务开始时的 commit")
    start.add_argument("--project", required=True)
    start.add_argument("--task", required=True)
    start.add_argument("--repo", default=None)
    start.add_argument("--app", default=None)
    start.add_argument("--test", default=None)
    start.add_argument("--adopt", action="store_true", help="把当前没保存的修改算进这个任务")
    start.add_argument("--stash", action="store_true", help="先把当前没保存的修改放一边")

    finish = sub.add_parser("finish", help="由脚本提交这个任务的改动")
    finish.add_argument("--project", required=True)
    finish.add_argument("--task", required=True)
    finish.add_argument("--repo", default=None)
    finish.add_argument("--app", default=None)
    finish.add_argument("--test", default=None)

    status = sub.add_parser("status", help="查看从 git 算出的改动对照")
    status.add_argument("--project", required=True)
    status.add_argument("--app", default=None)
    status.add_argument("--test", default=None)
    status.add_argument("--repo", default=None)

    preview = sub.add_parser("preview-revert", help="用大白话说明撤回，并先在临时副本里试一次")
    preview.add_argument("--project", required=True)
    preview.add_argument("--task", required=True)
    preview.add_argument("--repo", default=None)
    preview.add_argument("--app", default=None)
    preview.add_argument("--test", default=None)

    revert = sub.add_parser("revert", help="确认后撤回任务（保留历史）")
    revert.add_argument("--project", required=True)
    revert.add_argument("--task", required=True)
    revert.add_argument("--repo", default=None)
    revert.add_argument("--app", default=None)
    revert.add_argument("--test", default=None)
    revert.add_argument("--confirm", action="store_true")
    revert.add_argument("--stash", action="store_true")

    init_parser = sub.add_parser("init", help="只有用户同意后才 git init")
    init_parser.add_argument("--repo", required=True)
    init_parser.add_argument("--agree", action="store_true")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 1
    try:
        if args.command == "start":
            payload = start_task(args.project, args.task, repo=args.repo, adopt=args.adopt, stash=args.stash, app_file=args.app, test_file=args.test)
        elif args.command == "finish":
            payload = finish_task(args.project, args.task, repo=args.repo, app_file=args.app, test_file=args.test)
        elif args.command == "status":
            payload = ok("status", "已根据 git 算出改动。", "Computed changes from git.", observation=build_observation(args.project, args.app, args.repo, test_file=args.test))
        elif args.command == "preview-revert":
            payload = preview_revert(args.project, args.task, repo=args.repo, app_file=args.app, test_file=args.test)
        elif args.command == "revert":
            payload = execute_revert(args.project, args.task, repo=args.repo, app_file=args.app, test_file=args.test, confirm=args.confirm, stash=args.stash)
        elif args.command == "init":
            payload = init_repository(args.repo, agree=args.agree)
        else:
            payload = fail("unknown", "不认识这个命令。", "Unknown command.")
    except TrackError as exc:
        payload = fail(exc.code, exc.message_zh, exc.message_en, **exc.extra)
    return _print_payload(payload, args.json, args.lang)


CHANGE_PANEL_JS = r"""
const changeCopy = {
    zh: {
        files: '实际改了这些文件',
        plan: '这轮计划要改的功能',
        feature: '所属功能',
        noFiles: '这次没有改到代码文件',
        notStarted: '还没有开始记录这次任务的改动',
        inProgress: '正在做。下面是目前已经改过的文件，结束时会记成一个版本。',
        noPlan: '这轮还没有写计划要改的功能',
        noFeature: '还没关联功能',
        revert: '撤回这次修改',
        reverted: '已经撤回',
        staticRevert: '要撤回请打开网页模式',
        later: '后来的任务也改过这些文件',
        unattributedTitle: '未归属改动',
        unattributedHint: '这些提交没有归到单独的任务，只能整次一起撤回。',
        initTitle: '还没有版本记录',
        initAction: '我同意，开始记录版本',
        cancel: '先不撤回',
        confirm: '确认撤回',
        stash: '先放一边，再撤回',
        close: '知道了',
        working: '正在处理…'
    },
    en: {
        files: 'Files actually changed',
        plan: 'What this round planned to change',
        feature: 'Feature',
        noFiles: 'No code files changed',
        notStarted: 'This task has not been recorded yet',
        inProgress: 'In progress. These files have changed so far and will be saved as one version at the end.',
        noPlan: 'This round has no planned features yet',
        noFeature: 'No feature linked',
        revert: 'Revert this change',
        reverted: 'Reverted',
        staticRevert: 'Open web mode to revert',
        later: 'A later task also changed these files',
        unattributedTitle: 'Unattributed changes',
        unattributedHint: 'These commits are not tied to a single task and can only be reverted together.',
        initTitle: 'No version history yet',
        initAction: 'I agree, start recording versions',
        cancel: 'Not now',
        confirm: 'Revert',
        stash: 'Set my edits aside, then revert',
        close: 'OK',
        working: 'Working…'
    }
};

function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (ch) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch];
    });
}

function changeLang() {
    return changeCopy[currentLang] || changeCopy.zh;
}

function renderChangeChrome(data) {
    const banner = document.getElementById('change-banner');
    const extra = document.getElementById('unattributed-list');
    const copy = changeLang();
    const changes = (data && data.changes) || {};
    if (banner) {
        if (!changes.git_repo) {
            const button = (typeof DASHBOARD_MODE !== 'undefined' && DASHBOARD_MODE === 'web')
                ? `<button type="button" data-action="open-init" onclick="openInit()" class="mt-3 px-3 py-2 rounded-lg bg-white text-black text-sm font-semibold">${esc(copy.initAction)}</button>`
                : '';
            banner.innerHTML = `<div class="rounded-xl border border-zinc-700 bg-zinc-900/80 px-4 py-3 text-sm text-zinc-200"><p class="font-semibold text-white">${esc(copy.initTitle)}</p><p class="mt-1 text-zinc-400">${esc(currentLang === 'en' ? changes.message_en : changes.message_zh)}</p>${button}</div>`;
        } else {
            banner.innerHTML = '';
        }
    }
    if (!extra) return;
    const items = changes.unattributed || [];
    if (!changes.git_repo || !items.length) {
        extra.innerHTML = '';
        return;
    }
    extra.innerHTML = `<div class="rounded-xl border border-zinc-700 bg-zinc-900/60 px-4 py-3"><p class="text-sm font-semibold text-zinc-100">${esc(copy.unattributedTitle)}</p><p class="text-xs text-zinc-400 mt-1">${esc(copy.unattributedHint)}</p><div class="mt-3 space-y-2">${items.map(function (item) {
        const files = (item.files || []).map(function (file) { return esc(file.path); }).join('、') || esc(copy.noFiles);
        const button = (typeof DASHBOARD_MODE !== 'undefined' && DASHBOARD_MODE === 'web')
            ? `<button type="button" data-action="revert" data-revert-task="unattributed:${esc(item.commit)}" onclick="openRevert(this.getAttribute('data-revert-task'))" class="shrink-0 px-3 py-1.5 rounded-lg border border-zinc-600 text-xs text-zinc-100">${esc(copy.revert)}</button>`
            : `<span class="text-[11px] text-zinc-500">${esc(copy.staticRevert)}</span>`;
        return `<div class="flex items-start justify-between gap-3 text-xs text-zinc-300"><div><p class="font-medium text-zinc-100">${esc(item.subject)}</p><p class="mt-1 text-zinc-400">${files}</p></div>${button}</div>`;
    }).join('')}</div></div>`;
}

function renderTaskChanges(task, iter, changes) {
    const copy = changeLang();
    const obs = changes && changes.tasks && changes.tasks[task.task_id];
    if (!obs) {
        if (changes && !changes.git_repo) {
            const planned = ((iter && iter.modules) || []).map(function (mod) { return esc(mod.module_name || mod.module_id); });
            return `<div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs" data-change-panel="1"><div><p class="uppercase tracking-wide text-zinc-500">${esc(copy.files)}</p><p class="mt-1 text-zinc-400">${esc(currentLang === 'en' ? (changes.message_en || '') : (changes.message_zh || ''))}</p></div><div><p class="uppercase tracking-wide text-zinc-500">${esc(copy.plan)}</p>${planned.length ? `<ul class="mt-1 space-y-1 text-zinc-300">${planned.map(function (name) { return `<li>${name}</li>`; }).join('')}</ul>` : `<p class="mt-1 text-zinc-500">${esc(copy.noPlan)}</p>`}</div></div>`;
        }
        return '';
    }
    const files = obs.changed_files || [];
    const fileItems = files.length
        ? `<ul class="mt-1 space-y-1 text-zinc-200">${files.map(function (file) {
            const label = currentLang === 'en' ? file.label_en : file.label_zh;
            return `<li><span class="font-mono text-[12px]">${esc(file.path)}</span> <span class="text-zinc-500">${esc(label)}</span></li>`;
        }).join('')}</ul>`
        : `<p class="mt-1 text-zinc-500">${esc(obs.start_commit ? copy.noFiles : copy.notStarted)}</p>`;
    const features = (obs.belongs_to || []).map(function (item) { return esc(item.module_name); });
    const planned = (obs.planned || []).map(function (item) { return esc(item.module_name || item.module_id); });
    const notice = currentLang === 'en' ? obs.notice_en : obs.notice_zh;
    const noticeHtml = notice
        ? `<p class="mt-2 text-xs text-amber-200/90 bg-amber-500/10 border border-amber-500/20 rounded-lg px-3 py-2" data-notice="${obs.unplanned ? 'unplanned' : 'info'}">${esc(notice)}</p>`
        : '';
    const later = obs.later_tasks || [];
    const laterHtml = later.length
        ? `<p class="mt-2 text-xs text-zinc-300">${esc(copy.later)}：${later.map(function (item) { return esc(item.task_name); }).join(currentLang === 'en' ? ', ' : '、')}</p>`
        : '';
    let action = '';
    if (obs.reverted) {
        action = `<span class="text-[11px] text-amber-300">${esc(copy.reverted)}</span>`;
    } else if (obs.revertible && typeof DASHBOARD_MODE !== 'undefined' && DASHBOARD_MODE === 'web') {
        action = `<button type="button" data-action="revert" data-revert-task="${esc(task.task_id)}" onclick="openRevert(this.getAttribute('data-revert-task'))" class="px-3 py-1.5 rounded-lg bg-white text-black text-xs font-semibold">${esc(copy.revert)}</button>`;
    } else if (obs.revertible) {
        action = `<span class="text-[11px] text-zinc-500">${esc(copy.staticRevert)}</span>`;
    }
    const progress = obs.state === 'in_progress' ? `<p class="mt-2 text-xs text-blue-300">${esc(copy.inProgress)}</p>` : '';
    return `<div class="mt-3" data-change-panel="1" data-task-id="${esc(task.task_id)}"><div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs"><div><p class="uppercase tracking-wide text-zinc-500">${esc(copy.files)}</p>${fileItems}<p class="mt-2 text-zinc-400">${esc(copy.feature)}：${features.length ? features.join(currentLang === 'en' ? ', ' : '、') : esc(copy.noFeature)}</p></div><div><p class="uppercase tracking-wide text-zinc-500">${esc(copy.plan)}</p>${planned.length ? `<ul class="mt-1 space-y-1 text-zinc-300">${planned.map(function (name) { return `<li>${name}</li>`; }).join('')}</ul>` : `<p class="mt-1 text-zinc-500">${esc(copy.noPlan)}</p>`}</div></div>${progress}${noticeHtml}${laterHtml}<div class="mt-3">${action}</div></div>`;
}

function ensureRevertModal() {
    return document.getElementById('revert-modal');
}

function showModal(title, paragraphs, actions) {
    const modal = ensureRevertModal();
    if (!modal) return;
    document.getElementById('revert-modal-title').textContent = title;
    const body = document.getElementById('revert-modal-body');
    body.innerHTML = (paragraphs || []).map(function (line) {
        return `<p>${esc(line)}</p>`;
    }).join('');
    document.getElementById('revert-modal-actions').innerHTML = actions;
    modal.classList.remove('hidden');
}

function closeRevertModal() {
    const modal = document.getElementById('revert-modal');
    if (modal) modal.classList.add('hidden');
}

function openInit() {
    const copy = changeLang();
    const paragraphs = currentLang === 'en'
        ? ['Start recording versions in this project? This creates a Git repository and saves the current files as the starting point. Nothing is uploaded.', 'Revert stays hidden until you agree. Database changes, installed dependencies, and anything already published still cannot be reverted later.']
        : ['要开始在这个项目里记录版本吗？这会创建 Git 仓库，并把当前文件保存为起点。不会上传到网上。', '你不同意的话，撤回按钮不会出现。以后能撤回的也只是代码文件，数据库改动、已经安装的依赖和已经发布的内容仍然撤不回来。'];
    showModal(copy.initTitle, paragraphs, `<button type="button" data-action="agree-init" onclick="agreeInit()" class="px-4 py-2 rounded-lg bg-white text-black text-sm font-semibold">${esc(copy.initAction)}</button><button type="button" data-action="cancel-revert" onclick="closeRevertModal()" class="px-4 py-2 rounded-lg border border-zinc-600 text-sm">${esc(copy.cancel)}</button>`);
}

function agreeInit() {
    fetch('/api/git/init', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ agree: true }) })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            const paragraphs = [currentLang === 'en' ? (data.message_en || '') : (data.message_zh || '')];
            showModal(changeLang().initTitle, paragraphs, `<button type="button" data-action="cancel-revert" onclick="closeRevertModal(); refreshData();" class="px-4 py-2 rounded-lg bg-white text-black text-sm font-semibold">${esc(changeLang().close)}</button>`);
        });
}

function openRevert(taskId) {
    const copy = changeLang();
    showModal(copy.working, [copy.working], '');
    fetch('/api/revert/preview', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ task_id: taskId }) })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            const paragraphs = (data.paragraphs && (currentLang === 'en' ? data.paragraphs.en : data.paragraphs.zh)) || [currentLang === 'en' ? data.message_en : data.message_zh];
            let actions = `<button type="button" data-action="cancel-revert" onclick="closeRevertModal()" class="px-4 py-2 rounded-lg border border-zinc-600 text-sm">${esc(data.conflict ? copy.close : copy.cancel)}</button>`;
            if (data.can_revert) {
                actions = `<button type="button" data-action="confirm-revert" onclick="executeRevert('${esc(taskId)}', false)" class="px-4 py-2 rounded-lg bg-white text-black text-sm font-semibold">${esc(copy.confirm)}</button>` + actions;
            } else if (data.needs_stash) {
                actions = `<button type="button" data-action="stash-revert" onclick="executeRevert('${esc(taskId)}', true)" class="px-4 py-2 rounded-lg bg-white text-black text-sm font-semibold">${esc(copy.stash)}</button>` + actions;
            }
            showModal(copy.revert, paragraphs, actions);
        })
        .catch(function () {
            showModal(copy.revert, [currentLang === 'en' ? 'Could not open the confirmation.' : '确认说明没有打开。项目没有被改。'], `<button type="button" onclick="closeRevertModal()" class="px-4 py-2 rounded-lg border border-zinc-600 text-sm">${esc(copy.close)}</button>`);
        });
}

function executeRevert(taskId, stash) {
    const copy = changeLang();
    fetch('/api/revert/execute', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ task_id: taskId, confirm: true, stash: stash }) })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            const paragraphs = (data.paragraphs && (currentLang === 'en' ? data.paragraphs.en : data.paragraphs.zh)) || [currentLang === 'en' ? data.message_en : data.message_zh];
            if (!data.ok && data.paragraphs) {
                showModal(paragraphs[0] || copy.revert, paragraphs, `<button type="button" data-action="cancel-revert" onclick="closeRevertModal()" class="px-4 py-2 rounded-lg border border-zinc-600 text-sm">${esc(copy.close)}</button>`);
                return;
            }
            showModal(copy.revert, [currentLang === 'en' ? (data.message_en || '') : (data.message_zh || '')], `<button type="button" data-action="cancel-revert" onclick="closeRevertModal(); refreshData();" class="px-4 py-2 rounded-lg bg-white text-black text-sm font-semibold">${esc(copy.close)}</button>`);
            if (data.ok) refreshData();
        });
}
"""

REVERT_MODAL_HTML = """
<div id="revert-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4" style="background: rgba(0,0,0,.72)">
    <div class="w-full max-w-xl rounded-2xl border border-zinc-700 bg-zinc-900 p-6 shadow-2xl" role="dialog" aria-modal="true" aria-labelledby="revert-modal-title">
        <h3 id="revert-modal-title" class="text-xl font-bold text-white mb-4"></h3>
        <div id="revert-modal-body" class="space-y-3 text-base leading-7 text-zinc-100"></div>
        <div id="revert-modal-actions" class="mt-6 flex flex-wrap gap-3"></div>
    </div>
</div>
"""


if __name__ == "__main__":
    sys.exit(main())
