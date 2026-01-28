# Cox Skill FAQ and Troubleshooting

## Table of Contents
- [JSON File Format Issues](#1-json-file-format-issues)
- [Module ID Inconsistency Issues](#2-module-id-inconsistency-issues)
- [File Permission Issues](#3-file-permission-issues)
- [Experience Summary](#experience-summary)

---

## 1. JSON File Format Issues

### Problem Manifestation
When generating observability interface, JSON decoding error occurs, prompting "Extra data".

### Impact
- Unable to generate project observability interface
- Affects project progress tracking

### Root Cause
File contains invisible characters and encoding issues, possibly due to:
- Encoding conversion errors during file creation
- Special characters introduced during manual editing
- Format issues from copy-paste operations

### Troubleshooting Methods

#### Method 1: Use cat -A to View Invisible Characters
```bash
cat -A project_data.json
```
If seeing `^M`, `^I` or other special characters, encoding issues exist.

#### Method 2: Use Python to Validate JSON Format
```bash
python -m json.tool project_data.json > /dev/null
```
If returns error message, JSON format has issues.

#### Method 3: Use Python to Read and Rewrite
```python
import json

with open('project_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('project_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### Resolution Method
1. **Use cat -A to view actual file content**, discover massive invisible characters
2. **Recreate file and overwrite content**, clear invisible characters
3. **Use python -m json.tool to verify JSON format correctness**

### Preventive Measures
- Use scripts to generate data, avoid manual editing
- Use UTF-8 encoding supported editors when editing JSON files
- Avoid copy-pasting JSON content from untrusted sources

---

## 2. Module ID Inconsistency Issues

### Problem Manifestation
Module IDs in app_status.json don't match module IDs in project_data.json.

### Impact
- Observability interface cannot correctly correlate project data and application status data
- Module maturity information cannot display correctly

### Root Cause
Initially generated data files used default "example modules", but manual modification of project_data.json used new module names, causing module information inconsistency between two files.

### Example Problem

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

### Resolution Method
1. **Unify module IDs and names in both files**
2. **Ensure Calculation Core Module and User Interface Module remain consistent in both files**

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
    print(f"Modules in project_data.json: {project_modules}")
    print(f"Modules in app_status.json: {app_modules}")
else:
    print("✅ Modules consistent")
```

### Preventive Measures
- Use `--modules` parameter to define all modules at once, ensuring both files use same module list
- When modifying module information, synchronously update both files
- After generating data, use check script to verify module consistency

---

## 3. File Permission Issues

### Problem Manifestation
Unable to directly delete or modify certain files.

### Impact
- Unable to clean corrupted files through conventional methods
- Unable to update data files

### Root Cause
- Improper file system permission settings
- File locked by other process
- Insufficient file owner permissions

### Troubleshooting Methods
```bash
# View file permissions
ls -la project_data.json

# Check if file is locked
lsof project_data.json
```

### Resolution Method

#### Method 1: Use Python Code to Replace bash Commands
```python
import os

# Delete file
if os.path.exists('project_data.json'):
    os.remove('project_data.json')
    print("File deleted")
```

#### Method 2: Overwrite File Content via Edit Mode
```python
import json

with open('project_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

#### Method 3: Modify File Permissions (if needed)
```bash
chmod 644 project_data.json
```

### Preventive Measures
- Avoid attempting to modify files while being used by other processes
- Use appropriate file permissions (644 sufficient for data files)
- Avoid creating files as root user, causing subsequent permission issues

---

## Experience Summary

### Data Consistency
**Principle**: When using Cox skill, must ensure data consistency across all data files, especially module ID and name matching.

**Key Files**:
- `project_data.json`: Project iteration and task data
- `app_status.json`: Application module status data
- `test_metrics.json`: Test instrumentation and anomaly data

**Consistency Checklist**:
- [ ] Module IDs consistent in both files
- [ ] Module names consistent in both files
- [ ] Task-referenced module IDs exist in app_status.json
- [ ] All JSON files have correct format

### Format Validation
**Principle**: Before generating observability interface, should first verify all JSON files have correct format.

**Validation Steps**:
1. Use `python -m json.tool` to validate each JSON file
2. Use check script to verify module consistency
3. Confirm correctness before invoking `run_web_observability.py`

**Automated Validation Script**:
```bash
#!/bin/bash
echo "Validating JSON format..."

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
**Principle**: When handling JSON files containing Chinese characters, pay special attention to encoding issues, avoid invisible character occurrence.

**Precautions**:
- Always use UTF-8 encoding
- Choose UTF-8 supported editors (VS Code, Sublime Text, etc.)
- Avoid using Windows Notepad to edit JSON files
- When saving, choose "UTF-8 without BOM" format

**Check Encoding**:
```bash
file -i project_data.json
# Output should be: project_data.json: text/plain; charset=utf-8
```

### Fault Tolerance Mechanism
**Principle**: When encountering file operation issues, should try multiple methods to resolve, rather than limiting to single approach.

**Multiple Methods Comparison**:

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| Bash commands | Simple file operations | Fast and direct | Easily limited by permissions |
| Python os module | Cross-platform | Good compatibility | Code slightly complex |
| Python json module | JSON files | Auto-validates format | Only applicable to JSON |
| Manual editor | Need precise control | Flexible | Prone to introduce errors |

**Recommended Practice**:
- Prioritize using scripts to generate data, avoid manual editing
- When file operations fail, try using Python instead of bash
- Keep scripts cross-platform compatible (Linux/macOS/Windows)

---

## Common Error Codes Quick Reference

| Error Message | Possible Cause | Resolution |
|---------------|----------------|------------|
| `Extra data` | JSON format error, invisible characters | Use Python to rewrite file |
| `Expecting property name` | JSON syntax error (missing quotes) | Check JSON syntax |
| `Invalid escape sequence` | Escape character error | Use Python to write, ensure correct escaping |
| `Permission denied` | Insufficient file permissions | Check and modify file permissions |
| `FileNotFoundError` | File doesn't exist | Check if file path correct |
| `Module ID not found` | Module ID inconsistency | Unify module IDs in both files |

---

## Getting Help

If encountering issues not listed in this document, please:

1. Check detailed instructions in SKILL.md
2. View script help information: `python scripts/generate_observability_data.py --help`
3. Use validation scripts to check data consistency
4. View log files (if any) for more error information
