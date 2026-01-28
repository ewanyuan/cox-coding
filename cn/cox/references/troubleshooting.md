# Cox 技能常见问题与故障排查

## 目录
- [JSON 文件格式问题](#1-json-文件格式问题)
- [模块 ID 不一致问题](#2-模块-id-不一致问题)
- [文件权限问题](#3-文件权限问题)
- [经验总结](#经验总结)

---

## 1. JSON 文件格式问题

### 问题表现
生成可观测界面时出现 JSON 解码错误，提示 "Extra data"。

### 导致情况
- 无法生成项目可观测界面
- 影响项目进度跟踪

### 根本原因
文件中存在不可见字符和编码问题，可能是由于：
- 文件创建过程中的编码转换错误
- 手动编辑文件时引入的特殊字符
- 复制粘贴时的格式问题

### 排查方法

#### 方法 1：使用 cat -A 查看不可见字符
```bash
cat -A project_data.json
```
如果看到 `^M`、`^I` 或其他特殊字符，说明存在编码问题。

#### 方法 2：使用 Python 验证 JSON 格式
```bash
python -m json.tool project_data.json > /dev/null
```
如果返回错误信息，说明 JSON 格式有问题。

#### 方法 3：使用 Python 读取并重新写入
```python
import json

with open('project_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('project_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 修改方法
1. **使用 cat -A 查看文件的实际内容**，发现存在大量不可见字符
2. **重新创建文件并覆盖内容**，清除不可见字符
3. **使用 python -m json.tool 验证 JSON 格式正确性**

### 预防措施
- 使用脚本生成数据，避免手动编辑
- 编辑 JSON 文件时使用支持 UTF-8 编码的编辑器
- 避免从不信任的来源复制粘贴 JSON 内容

---

## 2. 模块 ID 不一致问题

### 问题表现
app_status.json 中的模块 ID 与 project_data.json 中的模块 ID 不匹配。

### 导致情况
- 可观测界面无法正确关联项目数据和应用状态数据
- 模块成熟度信息无法正确显示

### 根本原因
初始生成的数据文件使用了默认的"示例模块"，而手动修改 project_data.json 时使用了新的模块名称，导致两个文件中的模块信息不一致。

### 示例问题

**project_data.json**：
```json
{
  "iterations": [
    {
      "modules": [
        {"module_id": "MOD-001", "module_name": "UI界面模块"},
        {"module_id": "MOD-002", "module_name": "计算逻辑模块"}
      ]
    }
  ]
}
```

**app_status.json**（不一致）：
```json
{
  "modules": [
    {"module_id": "MOD-001", "module_name": "示例模块"},  // ❌ 名称不匹配
    {"module_id": "MOD-002", "module_name": "用户管理模块"}  // ❌ 模块不同
  ]
}
```

### 修改方法
1. **统一两个文件中的模块 ID 和名称**
2. **确保计算核心模块和用户界面模块在两个文件中保持一致**

#### 正确示例

**project_data.json**：
```json
{
  "iterations": [
    {
      "modules": [
        {"module_id": "MOD-001", "module_name": "UI界面模块"},
        {"module_id": "MOD-002", "module_name": "计算逻辑模块"}
      ]
    }
  ]
}
```

**app_status.json**（一致）：
```json
{
  "modules": [
    {"module_id": "MOD-001", "module_name": "UI界面模块"},   // ✅ 一致
    {"module_id": "MOD-002", "module_name": "计算逻辑模块"} // ✅ 一致
  ]
}
```

### 自动化检查脚本
```python
import json

# 读取两个文件
with open('project_data.json', 'r', encoding='utf-8') as f:
    project_data = json.load(f)

with open('app_status.json', 'r', encoding='utf-8') as f:
    app_data = json.load(f)

# 提取模块信息
project_modules = set()
for iteration in project_data['iterations']:
    for module in iteration['modules']:
        project_modules.add((module['module_id'], module['module_name']))

app_modules = set()
for module in app_data['modules']:
    app_modules.add((module['module_id'], module['module_name']))

# 检查一致性
if project_modules != app_modules:
    print("❌ 模块不一致！")
    print(f"project_data.json 中的模块: {project_modules}")
    print(f"app_status.json 中的模块: {app_modules}")
else:
    print("✅ 模块一致")
```

### 预防措施
- 使用 `--modules` 参数一次性定义所有模块，确保两个文件使用相同的模块列表
- 修改模块信息时，同步更新两个文件
- 生成数据后，使用检查脚本验证模块一致性

---

## 3. 文件权限问题

### 问题表现
无法直接删除或修改某些文件。

### 导致情况
- 无法通过常规方式清理损坏的文件
- 无法更新数据文件

### 根本原因
- 文件系统权限设置不当
- 文件被其他进程锁定
- 文件所有者权限不足

### 排查方法
```bash
# 查看文件权限
ls -la project_data.json

# 查看文件是否被锁定
lsof project_data.json
```

### 修改方法

#### 方法 1：使用 Python 代码替代 bash 命令
```python
import os

# 删除文件
if os.path.exists('project_data.json'):
    os.remove('project_data.json')
    print("文件已删除")
```

#### 方法 2：通过编辑模式覆盖文件内容
```python
import json

with open('project_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

#### 方法 3：修改文件权限（如果需要）
```bash
chmod 644 project_data.json
```

### 预防措施
- 避免在文件被其他进程使用时尝试修改
- 使用适当的文件权限（644 对于数据文件足够）
- 避免以 root 用户创建文件，导致后续权限问题

---

## 经验总结

### 数据一致性
**原则**：在使用 Cox 技能时，必须确保所有数据文件之间的数据一致性，特别是模块 ID 和名称的匹配。

**关键文件**：
- `project_data.json`：项目迭代和任务数据
- `app_status.json`：应用模块状态数据
- `test_metrics.json`：测试埋点和异常数据

**一致性检查清单**：
- [ ] 模块 ID 在两个文件中一致
- [ ] 模块名称在两个文件中一致
- [ ] 任务引用的模块 ID 存在于 app_status.json 中
- [ ] 所有 JSON 文件格式正确

### 格式验证
**原则**：在生成可观测界面之前，应先验证所有 JSON 文件的格式正确性。

**验证步骤**：
1. 使用 `python -m json.tool` 验证每个 JSON 文件
2. 使用检查脚本验证模块一致性
3. 确认无误后再调用 `run_web_observability.py`

**自动化验证脚本**：
```bash
#!/bin/bash
echo "验证 JSON 格式..."

for file in project_data.json app_status.json test_metrics.json; do
    echo -n "检查 $file... "
    if python -m json.tool $file > /dev/null 2>&1; then
        echo "✅"
    else
        echo "❌ 格式错误"
        exit 1
    fi
done

echo "所有文件格式正确"
```

### 编码问题
**原则**：在处理包含中文字符的 JSON 文件时，要特别注意编码问题，避免不可见字符的出现。

**注意事项**：
- 始终使用 UTF-8 编码
- 编辑器选择支持 UTF-8 的工具（VS Code、Sublime Text 等）
- 避免使用 Windows 记事本编辑 JSON 文件
- 保存时选择 "UTF-8 without BOM" 格式

**检查编码**：
```bash
file -i project_data.json
# 输出应为：project_data.json: text/plain; charset=utf-8
```

### 容错机制
**原则**：当遇到文件操作问题时，应尝试多种方法来解决，而不是局限于单一方式。

**多种方法对比**：

| 方法 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| Bash 命令 | 简单文件操作 | 快速直接 | 容易受权限限制 |
| Python os 模块 | 跨平台 | 兼容性好 | 代码稍复杂 |
| Python json 模块 | JSON 文件 | 自动验证格式 | 仅适用于 JSON |
| 编辑器手动 | 需要精确控制 | 灵活 | 容易引入错误 |

**推荐做法**：
- 优先使用脚本生成数据，避免手动编辑
- 文件操作失败时，尝试使用 Python 替代 bash
- 保持脚本跨平台兼容（Linux/macOS/Windows）

---

## 常见错误代码速查

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| `Extra data` | JSON 格式错误，不可见字符 | 使用 Python 重新写入文件 |
| `Expecting property name` | JSON 语法错误（缺少引号） | 检查 JSON 语法 |
| `Invalid escape sequence` | 转义字符错误 | 使用 Python 写入，确保正确转义 |
| `Permission denied` | 文件权限不足 | 检查并修改文件权限 |
| `FileNotFoundError` | 文件不存在 | 检查文件路径是否正确 |
| `Module ID not found` | 模块 ID 不一致 | 统一两个文件中的模块 ID |

---

## 获取帮助

如果遇到未在本文档中列出的问题，请：

1. 检查 SKILL.md 中的详细说明
2. 查看脚本的帮助信息：`python scripts/generate_observability_data.py --help`
3. 使用验证脚本检查数据一致性
4. 查看日志文件（如果有）以获取更多错误信息
