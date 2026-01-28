# Skill Optimization Guide

## Table of Contents
- [Optimization Types](#optimization-types)
- [Feasibility Assessment](#feasibility-assessment)
- [Test Standards](#test-standards)
- [Version Number Management](#version-number-management)
- [Best Practices](#best-practices)

## Optimization Types

### format_improvement
**Description**: Improve skill file format

**Common Scenarios**:
- SKILL.md frontmatter format non-compliant
- Lacks necessary fields (such as version)
- Directory structure doesn't comply with specifications
- File naming doesn't comply with specifications

**Optimization Strategy**:
- Fix YAML format errors
- Add missing fields
- Adjust directory structure
- Standardize file naming

**Risk Level**: Low

### content_optimization
**Description**: Optimize skill content

**Common Scenarios**:
- Redundant documentation content
- Unclear descriptions
- Outdated examples
- Lacks necessary usage guidance

**Optimization Strategy**:
- Delete redundant content
- Supplement necessary descriptions
- Update outdated examples
- Add best practices

**Risk Level**: Medium

### version_update
**Description**: Update skill version number

**Common Scenarios**:
- Initial skill needs version number added
- After optimization complete, update version number

**Optimization Strategy**:
- Follow semantic versioning specification
- Select version type based on change type

**Risk Level**: Low

### bug_fix
**Description**: Fix errors in skills

**Common Scenarios**:
- Script syntax errors
- Documentation content errors
- Path reference errors
- Dependency version errors

**Optimization Strategy**:
- Fix script syntax
- Correct documentation content
- Update path references
- Adjust dependency versions

**Risk Level**: High

### feature_enhancement
**Description**: Enhance skill functionality

**Common Scenarios**:
- Add new functionality
- Extend existing capabilities
- Integrate new tools or services
- Improve user experience

**Optimization Strategy**:
- Design new feature implementation plan
- Update SKILL.md and scripts
- Add necessary reference documentation
- Update usage examples

**Risk Level**: High

## Feasibility Assessment

### Assessment Criteria

**1. Skill Integrity**
- Skill directory exists and complete
- SKILL.md format correct
- Necessary scripts and reference documentation exist

**2. Optimization Content Clear**
- Optimization objective clear
- Optimization content specific
- Impact scope controllable

**3. Technical Feasibility**
- Technical solution feasible
- Required resources available
- Risk controllable

**4. Compatibility**
- Doesn't break existing functionality
- Backward compatible
- Doesn't affect other skills

### Infeasible Situations

**Skill Directory Damaged**
- Skill directory doesn't exist
- SKILL.md severely damaged
- Key scripts lost

**Optimization Content Unclear**
- Optimization objective vague
- Optimization content too complex
- Impact scope difficult to assess

**Technical Infeasibility**
- Lacks necessary technical support
- Need to rewrite large amounts of code
- Technical risk too high

**Compatibility Issues**
- Breaks existing functionality
- Incompatible changes
- Affects other skills' dependencies

## Test Standards

### 1. SKILL.md Format Validation

**YAML Frontmatter Validation**
- Starts and ends with `---`
- Contains `name` field
- Contains `description` field
- Contains `version` field (if optimization involves version)
- `dependency` field format correct

**Body Validation**
- Not exceeding 500 lines
- Link depth not exceeding one layer
- Uses imperative tone
- Format compliant

### 2. Script Syntax Check

**Python Scripts**
- No syntax errors
- Imported modules available
- Function definitions complete
- Parameter definitions clear

**Bash Scripts**
- No syntax errors
- Commands available
- Paths correct
- Permissions correct

### 3. Directory Structure Validation

**Fixed Structure**
- SKILL.md exists
- scripts/ directory exists (optional, but required when have scripts)
- references/ directory exists (optional, but required when have reference docs)
- assets/ directory exists (optional, but required when have assets)

**Extra Files**
- No temporary files
- No cache files
- No log files

### 4. Dependency Integrity Check

**Python Dependencies**
- `dependency.python` field format correct
- Package name and version correct
- Doesn't include installation commands

**System Dependencies**
- `dependency.system` field format correct
- Commands valid
- Doesn't include Python package installation commands

### 5. Functionality Verification

**Core Functions**
- Main functions available
- Scripts executable
- Parameters correct

**Integration Testing**
- Normal integration with other skills
- Data format correct
- Path references correct

## Version Number Management

### Semantic Versioning Specification

Version number format: `v<major>.<minor>.<patch>`

**Major (主版本)**
- Major changes
- Incompatible API changes
- Removing important features
- Example: v1.0.0 -> v2.0.0

**Minor (次版本)**
- Feature enhancements
- Backward compatible new features
- Adding new feature points
- Example: v1.0.0 -> v1.1.0

**Patch (修订版本)**
- Bug fixes
- Minor improvements
- Format improvements
- Documentation updates
- Example: v1.0.0 -> v1.0.1

### Version Number Update Rules

**format_improvement**
- Version type: patch
- Example: v1.0.0 -> v1.0.1

**content_optimization**
- Version type: patch (minor improvement) or minor (significant improvement)
- Example: v1.0.0 -> v1.0.1 or v1.0.0 -> v1.1.0

**version_update**
- Version type: patch
- Example: none -> v1.0.0

**bug_fix**
- Version type: patch (minor bug) or minor (significant bug)
- Example: v1.0.0 -> v1.0.1 or v1.0.0 -> v1.1.0

**feature_enhancement**
- Version type: minor (minor feature) or major (major feature)
- Example: v1.0.0 -> v1.1.0 or v1.0.0 -> v2.0.0

### Initial Version Number

If skill has no version number, set to: `v1.0.0`

## Best Practices

### Before Optimization
1. Fully analyze optimization opportunities
2. Assess optimization feasibility
3. Clarify optimization objectives and scope
4. Assess optimization risks
5. Prepare rollback plan

### During Optimization
1. Always maintain backup
2. Proceed step by step, small steps fast
3. Keep task status synchronized
4. Record detailed optimization logs
5. Handle issues promptly

### After Optimization
1. Comprehensive test verification
2. Update documentation and examples
3. Notify user of new changes
4. Remind user to reload skill
5. Clean temporary files

### Version Management
1. Follow semantic versioning specification
2. Select version type based on change type
3. Keep version numbers incremental
4. Record version change log
5. Periodically clean expired backups

### Risk Control
1. Prioritize low-risk, high-value optimizations
2. Avoid batch optimizations
3. Major changes require user confirmation
4. Maintain compatibility
5. Prepare rollback plan

### User Experience
1. Provide clear optimization descriptions
2. Timely notify user of optimization results
3. Provide rollback options
4. Help user reload skill
5. Collect user feedback

## Optimization Examples

### Example 1: Add version Field
**Detection**: SKILL.md lacks version field

**Optimization Type**: version_update

**Optimization Steps**:
1. Backup skill
2. Add version: v1.0.0 to SKILL.md frontmatter
3. Test verification: SKILL.md format correct
4. Update task status: completed

**Risk Level**: Low

### Example 2: Fix Format Error
**Detection**: SKILL.md frontmatter format non-compliant

**Optimization Type**: format_improvement

**Optimization Steps**:
1. Backup skill
2. Fix YAML format
3. Update version number: v1.0.0 -> v1.0.1
4. Test verification: SKILL.md format correct
5. Update task status: completed

**Risk Level**: Low

### Example 3: Fix Script Syntax Error
**Detection**: Script has syntax error

**Optimization Type**: bug_fix

**Optimization Steps**:
1. Backup skill
2. Fix script syntax error
3. Update version number: v1.0.0 -> v1.0.1
4. Test verification: Script syntax correct
5. Update task status: completed

**Risk Level**: High

### Example 4: Add New Feature
**Detection**: Need to add new feature

**Optimization Type**: feature_enhancement

**Optimization Steps**:
1. Analyze feasibility
2. Design feature solution
3. Backup skill
4. Implement new feature
5. Update documentation
6. Update version number: v1.0.0 -> v1.1.0
7. Test verification
8. Update task status: completed

**Risk Level**: High
