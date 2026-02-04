# Cox Skill Common Issues and Troubleshooting

## Table of Contents
- [JSON File Format Issues](#1-json-file-format-issues)
- [Module ID Inconsistency Issues](#2-module-id-inconsistency-issues)
- [File Permission Issues](#3-file-permission-issues)
- [Experience Summary](#experience-summary)

---

## 1. JSON File Format Issues

### Problem Manifestation
JSON decoding error occurs when generating observable interface, showing "Extra data".

### Situations Caused
- Unable to generate project observable interface
- Affects project progress tracking

### Root Cause
File contains invisible characters and encoding issues, possibly due to:
- Encoding conversion errors during file creation
- Special characters introduced during manual editing
- Format issues from copy-paste operations

### Troubleshooting Methods

#### Method 1: Use cat -A to view invisible characters
```bash
cat -A project_data.json
```
If you see `^M`, `^I` or other special characters, encoding issues exist.

#### Method 2: Use Python to verify JSON format
```bash
python -m json.tool project_data.json > /dev/null
```
If error messages are returned, JSON format has issues.

#### Method 3: Use Python to read and rewrite
```python
import json

with open('project_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('project_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### Modification Methods
1. **Use cat -A to view actual file content**, discovering numerous invisible characters
2. **Recreate file and overwrite content**, clearing invisible characters
3. **Use python -m json.tool to verify JSON format correctness**

### Prevention Measures
- Use scripts to generate data, avoid manual editing
- Use editors supporting UTF-8 encoding when editing JSON files
- Avoid copying and pasting JSON content from untrusted sources

---

## 2. Module ID Inconsistency Issues

### Problem Manifestation
Module IDs in app_status.json do not match those in project_data.json.

### Situations Caused
- Observable interface unable to correctly associate project data and application status data
- Module maturity information unable to display correctly

### Root Cause
Initial generated data files used default "example modules", while manually modifying project_data.json used new module names, causing module information inconsistency between the two files.

### Example Problems

**project_data.json**:
```json
{
  "iterations": [
    {
      "modules": [
        {"module_id": "MOD-001", "module_name": "UI Interface Module"},
        {"module_id": "MOD-002", "module_name": "Calculation Logic Module"}
      ]
    }
  ]
}
```

**app_status.json** (inconsistent):
```json
{
  "modules": [
    {"module_id": "MOD-001", "module_name": "Example Module"},  // ❌ Name mismatch
    {"module_id": "MOD-002", "module_name": "User Management Module"}  // ❌ Different module
  ]
}
```

### Modification Methods
1. **Unify module IDs and names in both files**
2. **Ensure calculation core module and user interface module remain consistent in both files**

#### Correct Example

**project_data.json**:
```json
{
  "iterations": [
    {
      "modules": [
        {"module_id": "MOD-001", "module_name": "UI Interface Module"},
        {"module_id": "MOD-002", "module_name": "Calculation Logic Module"}
      ]
    }
  ]
}
```

**app_status.json** (consistent):
```json
{
  "modules": [
    {"module_id": "MOD-001", "module_name": "UI Interface Module"},   // ✅ Consistent
    {"module_id": "MOD-002", "module_name": "Calculation Logic Module"} // ✅ Consistent
  ]
}
```

### Automated Check Script
```python
import json

# Read both files
with open('project_data.json', 'r', encoding='utf-8') as f:
    project_data = json.load(f)

with open('app_status.json', 'r', encoding='utf-8') as f:
    app_data = json.load(f)

# Extract module information
project_modules = set()
for iteration in project_data['iterations']:
    for module in iteration['modules']:
        project_modules.add((module['module_id'], module['module_name']))

app_modules = set()
for module in app_data['modules']:
    app_modules.add((module['module_id'], module['module_name']))

# Check consistency
if project_modules != app_modules:
    print("❌ Module inconsistency!")
    print(f"project_data.json modules: {project_modules}")
    print(f"app_status.json modules: {app_modules}")
else:
    print("✅ Modules consistent")
```

### Prevention Measures
- Use `--modules` parameter to define all modules at once, ensuring both files use the same module list
- When modifying module information, update both files simultaneously
- After generating data, use check script to verify module consistency

---

## 3. File Permission Issues

### Problem Manifestation
Unable to directly delete or modify certain files.

### Situations Caused
- Unable to clean corrupted files via conventional methods
- Unable to update data files

### Root Cause
- Improper file system permission settings
- File locked by other processes
- Insufficient file owner permissions

### Troubleshooting Methods
```bash
# View file permissions
ls -la project_data.json

# View if file is locked
lsof project_data.json
```

### Modification Methods

#### Method 1: Use Python code instead of bash commands
```python
import os

# Delete file
if os.path.exists('project_data.json'):
    os.remove('project_data.json')
    print("File deleted")
```

#### Method 2: Overwrite file content through edit mode
```python
import json

with open('project_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

#### Method 3: Modify file permissions (if needed)
```bash
chmod 644 project_data.json
```

### Prevention Measures
- Avoid attempting modifications when file is used by other processes
- Use appropriate file permissions (644 sufficient for data files)
- Avoid creating files as root user, which causes subsequent permission issues

---

## Experience Summary

### Data Consistency
**Principle**: When using Cox skill, must ensure data consistency between all data files, especially matching of module IDs and names.

**Key Files**:
- `project_data.json`: Project iteration and task data
- `app_status.json`: Application module status data
- `test_metrics.json`: Test tracing points and anomaly data

**Consistency Check List**:
- [ ] Module IDs consistent in both files
- [ ] Module names consistent in both files
- [ ] Task-referenced module IDs exist in app_status.json
- [ ] All JSON file formats correct

### Format Validation
**Principle**: Before generating observable interface, should first verify format correctness of all JSON files.

**Verification Steps**:
1. Use `python -m json.tool` to verify each JSON file
2. Use check script to verify module consistency
3. Confirm no issues before calling `run_web_observability.py`

**Automated Verification Script**:
```bash
#!/bin/bash
echo "Verifying JSON format..."

for file in project_data.json app_status.json test_metrics.json; do
    echo -n "Checking $file... "
    if python -m json.tool $file > /dev/null 2>&1; then
        echo "✅"
    else
        echo "❌ Format error"
        exit 1
    fi
done

echo "All files format correct"
```

### Encoding Issues
**Principle**: When handling JSON files containing Chinese characters, pay special attention to encoding issues to avoid invisible characters.

**Considerations**:
- Always use UTF-8 encoding
- Choose editors supporting UTF-8 (VS Code, Sublime Text, etc.)
- Avoid editing JSON files with Windows Notepad
- Select "UTF-8 without BOM" format when saving

**Check Encoding**:
```bash
file -i project_data.json
# Output should be: project_data.json: text/plain; charset=utf-8
```

### Fault Tolerance Mechanism
**Principle**: When encountering file operation problems, try multiple methods to resolve rather than limiting to a single approach.

**Comparison of Multiple Methods**:

| Method | Applicable Scenario | Advantages | Disadvantages |
|--------|-------------------|------------|---------------|
| Bash Commands | Simple file operations | Fast and direct | Easily restricted by permissions |
| Python os Module | Cross-platform | Good compatibility | Code slightly complex |
| Python json Module | JSON files | Automatically validates format | Only applicable to JSON |
| Manual Editor | Need precise control | Flexible | Easy to introduce errors |

**Recommended Practice**:
- Prioritize script generation of data, avoid manual editing
- When file operations fail, try using Python instead of bash
- Maintain script cross-platform compatibility (Linux/macOS/Windows)

---

## Common Error Code Quick Reference

| Error Message | Possible Cause | Solution |
|---------------|----------------|----------|
| `Extra data` | JSON format error, invisible characters | Use Python to rewrite file |
| `Expecting property name` | JSON syntax error (missing quotes) | Check JSON syntax |
| `Invalid escape sequence` | Escape character error | Use Python to write, ensure proper escaping |
| `Permission denied` | Insufficient file permissions | Check and modify file permissions |
| `FileNotFoundError` | File does not exist | Check if file path is correct |
| `Module ID not found` | Module ID inconsistency | Unify module IDs in both files |

---

## Getting Help

If encountering issues not listed in this document, please:

1. Check detailed instructions in SKILL.md
2. View script help information: `python scripts/generate_observability_data.py --help`
3. Use verification script to check data consistency
4. Check log files (if any) for more error information