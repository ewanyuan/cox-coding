"""Temporary git repos for task recording, unplanned notices, and safe revert."""

import importlib.util
import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(params=["cn", "en"])
def tree(request):
    name = request.param
    base = ROOT / name
    track = load(base / "cox" / "scripts" / "task_track.py", f"track_{name}_{id(request)}")
    collect = load(base / "cox" / "scripts" / "collect_data.py", f"collect_{name}_{id(request)}")
    dashboard = load(base / "cox" / "scripts" / "run_web_observability.py", f"dash_{name}_{id(request)}")
    return {"name": name, "base": base, "track": track, "collect": collect, "dashboard": dashboard}


def git(repo, *args, check=True):
    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": "Tester",
        "GIT_AUTHOR_EMAIL": "tester@example.com",
        "GIT_COMMITTER_NAME": "Tester",
        "GIT_COMMITTER_EMAIL": "tester@example.com",
    })
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        env=env,
    )
    if check and result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return result


def seed_repo():
    repo = Path(tempfile.mkdtemp(prefix="cox-track-", dir="/tmp"))
    git(repo, "init", "-b", "main")
    (repo / "article_list.py").write_text("line\n", encoding="utf-8")
    (repo / "login.py").write_text("login\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "base")
    return repo


def write_data(repo, tasks, modules=None):
    if modules is None:
        modules = [
            {"module_id": "MOD-LIST", "module_name": "文章列表", "expected_completion": 1},
            {"module_id": "MOD-DETAIL", "module_name": "文章详情", "expected_completion": 1},
        ]
    project = {
        "project_name": "演示",
        "current_iteration": "ITER-1",
        "iterations": [{
            "iteration_id": "ITER-1",
            "iteration_name": "第一轮",
            "status": "in_progress",
            "tasks": tasks,
            "modules": modules,
            "assumptions": [],
        }],
    }
    app = {
        "app_name": "演示",
        "last_updated": "2026-10-26 00:00:00",
        "modules": [
            {"module_id": "MOD-LIST", "module_name": "文章列表", "status": "optimized", "completion_rate": 1.0},
            {"module_id": "MOD-LOGIN", "module_name": "登录", "status": "optimized", "completion_rate": 1.0},
        ],
    }
    test = {
        "last_updated": "2026-10-26 00:00:00",
        "test_suites": [],
        "tracing_points": [],
        "anomalies": [],
    }
    project_path = repo / "project_data.json"
    app_path = repo / "app_status.json"
    test_path = repo / "test_metrics.json"
    project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    app_path.write_text(json.dumps(app, ensure_ascii=False, indent=2), encoding="utf-8")
    test_path.write_text(json.dumps(test), encoding="utf-8")
    return project_path, app_path, test_path


def task_record(project_path, task_id):
    data = json.loads(project_path.read_text(encoding="utf-8"))
    for task in data["iterations"][0]["tasks"]:
        if task["task_id"] == task_id:
            return task
    raise AssertionError(task_id)


def run_task(track, repo, project, app, test, task_id, filename, content):
    started = track.start_task(str(project), task_id, repo=str(repo), app_file=str(app), test_file=str(test))
    assert started["ok"], started
    (repo / filename).write_text(content, encoding="utf-8")
    finished = track.finish_task(str(project), task_id, repo=str(repo), app_file=str(app), test_file=str(test))
    assert finished["ok"], finished
    return finished


def test_cn_en_tracker_and_validator_match():
    assert (ROOT / "cn/cox/scripts/task_track.py").read_bytes() == (ROOT / "en/cox/scripts/task_track.py").read_bytes()
    assert (ROOT / "cn/cox/scripts/collect_data.py").read_bytes() == (ROOT / "en/cox/scripts/collect_data.py").read_bytes()


def test_confirmed_meaning_and_has_issue(tree):
    validator = tree["collect"].DataValidator()
    assert validator.validate_app_status({
        "app_name": "演示",
        "last_updated": "2026-10-26 00:00:00",
        "modules": [{"module_name": "文章列表", "status": "has_issue", "issue_description": "不好看"}],
    })
    broken = tree["collect"].DataValidator()
    assert not broken.validate_app_status({
        "app_name": "演示",
        "last_updated": "2026-10-26 00:00:00",
        "modules": [{"module_name": "文章列表", "status": "not-a-status"}],
    })
    cn = (ROOT / "cn/cox/references/data_format.md").read_text(encoding="utf-8")
    en = (ROOT / "en/cox/references/data_format.md").read_text(encoding="utf-8")
    assert "待确认" in cn and "已确认完成" not in cn
    assert "Awaiting confirmation" in en and "Confirmed complete" not in en
    assert "has_issue" in cn and "has_issue" in en
    for readme in (ROOT / "cn/README.md", ROOT / "README.md", ROOT / "en/README.md"):
        text = readme.read_text(encoding="utf-8")
        assert "自动识别并保护" not in text
        assert "automatically identifying and protecting" not in text
        assert "automatically avoids" not in text


def test_no_pyc_tracked():
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    assert ".pyc" not in tracked
    assert "__pycache__" not in tracked
    assert "__pycache__/" in (ROOT / ".gitignore").read_text(encoding="utf-8")


def test_start_and_finish_record_the_commit(tree):
    track = tree["track"]
    repo = seed_repo()
    project, app, test = write_data(repo, [
        {"task_id": "TASK-1", "task_name": "实现文章列表", "status": "todo", "module_ids": ["MOD-LIST"]},
        {"task_id": "TASK-2", "task_name": "实现文章详情", "status": "todo", "module_ids": ["MOD-DETAIL"]},
    ])
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / "notes.txt").write_text("not yet", encoding="utf-8")
    refused = track.start_task(str(project), "TASK-1", repo=str(repo), app_file=str(app), test_file=str(test))
    assert not refused["ok"]
    assert refused["code"] == "dirty"
    assert (repo / "notes.txt").read_text(encoding="utf-8") == "not yet"
    (repo / "notes.txt").unlink()

    started = track.start_task(str(project), "TASK-1", repo=str(repo), app_file=str(app), test_file=str(test))
    assert started["ok"], started
    assert started["start_commit"] == head
    busy = track.start_task(str(project), "TASK-2", repo=str(repo), app_file=str(app), test_file=str(test))
    assert not busy["ok"]
    assert busy["code"] == "busy"
    assert "实现文章列表" in busy["message_zh"]
    assert task_record(project, "TASK-2")["status"] == "todo"

    (repo / "article_list.py").write_text("line\nlist\n", encoding="utf-8")
    finished = track.finish_task(str(project), "TASK-1", repo=str(repo), app_file=str(app), test_file=str(test))
    assert finished["ok"], finished
    record = task_record(project, "TASK-1")
    assert record["status"] == "done"
    assert record["start_commit"] == head
    assert record["end_commit"]
    body = git(repo, "log", "-1", "--format=%B", record["end_commit"]).stdout
    assert "Cox-Task: TASK-1" in body
    names = git(repo, "diff", "--name-only", record["start_commit"], record["end_commit"]).stdout
    assert "article_list.py" in names
    assert "project_data.json" not in names
    assert git(repo, "merge-base", "--is-ancestor", record["start_commit"], record["end_commit"]).returncode == 0


def test_changed_files_come_from_git_and_unplanned_notice(tree):
    track = tree["track"]
    repo = seed_repo()
    project, app, test = write_data(repo, [
        {"task_id": "TASK-LOGIN", "task_name": "顺手改登录", "status": "todo", "module_ids": ["MOD-LOGIN"]},
    ])
    run_task(track, repo, project, app, test, "TASK-LOGIN", "login.py", "login\nchanged\n")
    data = json.loads(project.read_text(encoding="utf-8"))
    data["iterations"][0]["tasks"][0]["changed_files"] = ["fake_from_ai.py"]
    project.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    observation = track.build_observation(str(project), str(app), str(repo))
    info = observation["tasks"]["TASK-LOGIN"]
    paths = [item["path"] for item in info["changed_files"]]
    assert paths == ["login.py"]
    assert info["unplanned"] is True
    assert "计划外" in info["notice_zh"]
    assert "不会阻止" in info["notice_zh"]
    assert "Unplanned" in info["notice_en"]
    assert "nothing is blocked" in info["notice_en"]
    assert any(item["module_name"] == "文章列表" for item in info["planned"])
    assert any(item["module_name"] == "登录" for item in info["belongs_to"])


def test_clean_revert_keeps_history_and_confirmation(tree):
    track = tree["track"]
    repo = seed_repo()
    project, app, test = write_data(repo, [
        {"task_id": "TASK-A", "task_name": "实现文章列表", "status": "todo", "module_ids": ["MOD-LIST"]},
        {"task_id": "TASK-B", "task_name": "实现文章详情", "status": "todo", "module_ids": ["MOD-DETAIL"]},
    ])
    run_task(track, repo, project, app, test, "TASK-A", "article_list.py", "line\nlist\n")
    run_task(track, repo, project, app, test, "TASK-B", "login.py", "login\ndetail\n")
    original = task_record(project, "TASK-A")["end_commit"]
    refused = track.execute_revert(str(project), "TASK-A", repo=str(repo), app_file=str(app), test_file=str(test), confirm=False)
    assert refused["code"] == "need_confirm"
    assert git(repo, "rev-parse", "HEAD").stdout.strip() != ""  # still a repo
    head_before = git(repo, "rev-parse", "HEAD").stdout.strip()
    preview = track.preview_revert(str(project), "TASK-A", repo=str(repo), app_file=str(app), test_file=str(test))
    assert preview["can_revert"] is True
    assert preview["conflict"] is False
    text = "\n".join(preview["paragraphs"]["zh"])
    english = "\n".join(preview["paragraphs"]["en"])
    assert "数据库" in text and "依赖" in text and "发布" in text
    assert "database" in english.lower() and "dependencies" in english.lower() and "published" in english.lower()
    done = track.execute_revert(str(project), "TASK-A", repo=str(repo), app_file=str(app), test_file=str(test), confirm=True)
    assert done["ok"], done
    assert (repo / "article_list.py").read_text(encoding="utf-8") == "line\n"
    assert "detail" in (repo / "login.py").read_text(encoding="utf-8")
    assert task_record(project, "TASK-A")["status"] == "reverted"
    assert task_record(project, "TASK-B")["status"] == "done"
    history = git(repo, "rev-list", "HEAD").stdout
    assert original in history
    assert git(repo, "rev-parse", "HEAD").stdout.strip() != head_before
    app_data = json.loads(app.read_text(encoding="utf-8"))
    article = next(item for item in app_data["modules"] if item["module_id"] == "MOD-LIST")
    assert article["status"] == "confirmed"


def test_conflicting_revert_stops_and_names_the_later_task(tree):
    track = tree["track"]
    repo = seed_repo()
    project, app, test = write_data(repo, [
        {"task_id": "TASK-A", "task_name": "实现文章列表", "status": "todo", "module_ids": ["MOD-LIST"]},
        {"task_id": "TASK-C", "task_name": "调整文章列表样式", "status": "todo", "module_ids": ["MOD-LIST"]},
    ])
    run_task(track, repo, project, app, test, "TASK-A", "article_list.py", "alpha\n")
    run_task(track, repo, project, app, test, "TASK-C", "article_list.py", "beta\n")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    status_before = git(repo, "status", "--porcelain").stdout
    preview = track.preview_revert(str(project), "TASK-A", repo=str(repo), app_file=str(app), test_file=str(test))
    assert preview["conflict"] is True
    assert preview["can_revert"] is False
    blob = json.dumps(preview, ensure_ascii=False)
    assert "调整文章列表样式" in blob
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == head
    assert git(repo, "status", "--porcelain").stdout == status_before
    assert (repo / "article_list.py").read_text(encoding="utf-8") == "beta\n"
    assert len(git(repo, "worktree", "list").stdout.splitlines()) == 1
    executed = track.execute_revert(str(project), "TASK-A", repo=str(repo), app_file=str(app), test_file=str(test), confirm=True)
    assert executed["ok"] is False
    assert executed["conflict"] is True
    assert "调整文章列表样式" in json.dumps(executed, ensure_ascii=False)
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == head
    assert (repo / "article_list.py").read_text(encoding="utf-8") == "beta\n"
    assert task_record(project, "TASK-A")["status"] == "done"


def test_uncommitted_changes_are_preserved(tree):
    track = tree["track"]
    repo = seed_repo()
    project, app, test = write_data(repo, [
        {"task_id": "TASK-A", "task_name": "实现文章列表", "status": "todo", "module_ids": ["MOD-LIST"]},
    ])
    run_task(track, repo, project, app, test, "TASK-A", "article_list.py", "line\nlist\n")
    (repo / "notes.txt").write_text("keep me\n", encoding="utf-8")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    blocked = track.execute_revert(str(project), "TASK-A", repo=str(repo), app_file=str(app), test_file=str(test), confirm=True)
    assert blocked["ok"] is False
    assert blocked["code"] == "dirty"
    assert (repo / "notes.txt").read_text(encoding="utf-8") == "keep me\n"
    assert (repo / "article_list.py").read_text(encoding="utf-8") == "line\nlist\n"
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == head
    restored = track.execute_revert(
        str(project), "TASK-A", repo=str(repo), app_file=str(app), test_file=str(test), confirm=True, stash=True
    )
    assert restored["ok"], restored
    assert (repo / "notes.txt").read_text(encoding="utf-8") == "keep me\n"
    assert (repo / "article_list.py").read_text(encoding="utf-8") == "line\n"


def test_non_git_project_does_not_init_without_agreement(tree):
    track = tree["track"]
    repo = Path(tempfile.mkdtemp(prefix="cox-nogit-", dir="/tmp"))
    project, app, test = write_data(repo, [
        {"task_id": "TASK-1", "task_name": "实现文章列表", "status": "todo", "module_ids": ["MOD-LIST"]},
    ])
    (repo / "article_list.py").write_text("line\n", encoding="utf-8")
    observation = track.build_observation(str(project), str(app), str(repo))
    assert observation["git_repo"] is False
    assert observation["revert_available"] is False
    assert "同意" in observation["message_zh"]
    preview = track.preview_revert(str(project), "TASK-1", repo=str(repo), app_file=str(app), test_file=str(test))
    assert preview["can_revert"] is False
    assert not (repo / ".git").exists()
    refused = track.init_repository(str(repo), agree=False)
    assert refused["ok"] is False
    assert not (repo / ".git").exists()
    agreed = track.init_repository(str(repo), agree=True)
    assert agreed["ok"], agreed
    assert (repo / ".git").exists()
    assert git(repo, "rev-parse", "HEAD").returncode == 0
    body = git(repo, "log", "-1", "--format=%B").stdout
    assert "Cox-Init: true" in body


def test_mixed_commit_reverts_together(tree):
    track = tree["track"]
    repo = seed_repo()
    project, app, test = write_data(repo, [
        {"task_id": "TASK-A", "task_name": "实现文章列表", "status": "todo", "module_ids": ["MOD-LIST"]},
        {"task_id": "TASK-B", "task_name": "补充文章列表", "status": "todo", "module_ids": ["MOD-LIST"]},
    ])
    run_task(track, repo, project, app, test, "TASK-A", "article_list.py", "line\nlist\n")
    run_task(track, repo, project, app, test, "TASK-B", "login.py", "login\nother\n")
    shared = task_record(project, "TASK-A")["end_commit"]
    data = json.loads(project.read_text(encoding="utf-8"))
    for task in data["iterations"][0]["tasks"]:
        task["end_commit"] = shared
    project.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    preview = track.preview_revert(str(project), "TASK-B", repo=str(repo), app_file=str(app), test_file=str(test))
    assert preview["can_revert"] is True
    together = {item["task_id"] for item in preview["together"]}
    assert together == {"TASK-A", "TASK-B"}
    assert "一起撤回" in "\n".join(preview["paragraphs"]["zh"])
    done = track.execute_revert(str(project), "TASK-B", repo=str(repo), app_file=str(app), test_file=str(test), confirm=True)
    assert done["ok"], done
    assert task_record(project, "TASK-A")["status"] == "reverted"
    assert task_record(project, "TASK-B")["status"] == "reverted"
    subjects = git(repo, "log", "--format=%s").stdout
    assert subjects.count("cox: revert") == 1


def test_dashboard_shows_files_plan_and_revert_copy(tree):
    track = tree["track"]
    dashboard = tree["dashboard"]
    repo = seed_repo()
    project, app, test = write_data(repo, [
        {"task_id": "TASK-LIST", "task_name": "实现文章列表", "status": "todo", "module_ids": ["MOD-LIST"]},
        {"task_id": "TASK-LOGIN", "task_name": "顺手改登录", "status": "todo", "module_ids": ["MOD-LOGIN"]},
    ])
    run_task(track, repo, project, app, test, "TASK-LIST", "article_list.py", "line\nlist\n")
    run_task(track, repo, project, app, test, "TASK-LOGIN", "login.py", "login\nchanged\n")
    dashboard.data_manager = dashboard.ObservabilityData(str(project), str(app), str(test), repo_hint=str(repo))
    client = dashboard.app.test_client()
    payload = client.get("/api/data").get_json()
    login = payload["changes"]["tasks"]["TASK-LOGIN"]
    assert [item["path"] for item in login["changed_files"]] == ["login.py"]
    assert login["unplanned"] is True
    assert "计划外" in login["notice_zh"]
    page = client.get("/").get_data(as_text=True)
    assert "renderTaskChanges" in page
    assert "DASHBOARD_MODE = 'web'" in page
    assert "实际改了这些文件" in page
    preview = client.post("/api/revert/preview", json={"task_id": "TASK-LOGIN"}).get_json()
    assert preview["can_revert"] is True
    assert "数据库" in "\n".join(preview["paragraphs"]["zh"])
    output = repo / "observability.html"
    dashboard.generate_static_html(dashboard.data_manager, str(output))
    static_html = output.read_text(encoding="utf-8")
    assert "计划外" in static_html
    assert "login.py" in static_html
    assert "DASHBOARD_MODE = 'static'" in static_html
    assert "REVERT_MODAL" not in static_html or 'id="revert-modal"' not in static_html
