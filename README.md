# Cox Programming: Your AI Coding Navigator

> Enabling non-technical users to maintain control over AI programming through data-driven thinking and systems thinking

---

## Common Challenges

You are a product manager, designer, entrepreneur, or simply have an idea you want to implement. You've heard that AI can help write code, so you eagerly start "Vibe Coding" — conversing with AI based on intuition, hoping it will magically transform your ideas into reality.

But soon, you encounter these challenges:

| Challenge | What You Experience | Why It Happens |
|-----------|---------------------|----------------|
| **Black Box Anxiety** | AI says "I'm done," but you have no idea what it did, which files it changed, or whether it broke something else | AI's thought process is invisible to you; you can only passively accept results |
| ** Fragmented Collaboration** | Fix one issue, create another. AI lacks global awareness, often breaking B while fixing A, leading to endless "fix-refix" cycles | Lack of systematic perspective; each modification is an isolated operation |
| **Progress Fog** | Ask AI "How's the project going?" and get a vague answer. You don't know true completion status or can identify risks | No data support; collaboration status relies entirely on AI's subjective judgment |
| **Repetitive Rework** | You clearly said "I'm happy with this feature," but AI changed it again during refactoring. Your feedback wasn't remembered | Human feedback isn't systematically recorded; AI cannot identify "satisfied" boundaries |
| **Capability Ceiling** | Can only ask AI to do one thing at a time. When facing complex problems requiring multi-step collaboration, AI "forgets" | AI capabilities are atomicized; cannot combine into more powerful system-level capabilities |
| **Knowledge Loss** | Project is done, but experience, rules, and best practices accumulated during the process are scattered in conversation history, unavailable for reuse | Implicit knowledge from collaboration isn't captured and structured |

---

## Our Solution: Deterministic AI Collaboration

**Core Principle**: AI collaboration should not be a black-box game of "feels right," but rather a **transparent, data-driven, systematically operating** deterministic process.

### Three Core Principles

#### 1. Transparent and Fluid Interaction Experience

```
Traditional Vibe Coding          Deterministic Collaboration
┌─────────────────────┐          ┌─────────────────────┐
│  You: Do this       │          │  AI: I observe project status │
│      ↓              │          │      Data presented to you     │
│  AI: OK             │    vs    │  You: Confirm/adjust direction │
│      ↓              │          │      ↓              │
│  ???Black Box???    │          │  AI: Execute & observe in real-time│
│      ↓              │          │      ↓              │
│  AI: Done           │          │  AI: Effect verification + improvement suggestions│
│      ↓              │          │      ↓              │
│  You: Broken, fix   │          │  You: Confirm/continue optimizing│
│      ↓              │          └─────────────────────┘
│  AI: Fixed          │
│      ↓              │
│  You: Still not changed??/also broken @_@ │
│      ↓              │
│  AI: (confident face) I found another problem! │
│      (infinite loop...)   │
└─────────────────────┘
```

**How?**
- AI helps you open the terminal, requests you to test, while observing the execution process simultaneously
- Displays test results and improvement suggestions in real-time
- All decisions based on actual execution data, not guesses
<img width="1017" height="366" alt="1_en" src="https://github.com/user-attachments/assets/6adf5c61-9870-4d72-b167-669004a54171" />


#### 2. Data-Driven Rules: Only Rules Based on Real Data Are Effective

Many people establish numerous rules before starting AI collaboration:
- "Code style should be consistent"
- "Functions should not exceed 50 lines"
- "Must have complete comments"

**But these rules are often ineffective** — because they're not derived from analysis of your project's actual runtime data.

**Characteristics of Effective Rules**:
```
Empty Rules (Ineffective)              Data-Driven Rules (Effective)
─────────────────          ─────────────────
"Code should be fast"     →        "Login API response time >800ms,
                           need to optimize database query"

"Don't have bugs"         →        "Test data shows 15% failure rate in user
                           registration flow, need to add payment
                           channel timeout handling"

"Code should be clear"    →        "Performance tracing shows checkout()
                           function accounts for 60% of execution time,
                           needs to be split"
```

**How?**
- Automatically collect data for you
- Establish rules based on real performance metrics, error rates, and user behavior data
- Optimizations and refactoring based on your project's runtime data are truly effective
<img width="1344" height="768" alt="2_en" src="https://github.com/user-attachments/assets/4eb0d092-b3ac-48e9-84f0-bc6a29c8fdfe" />


#### 3. Systematic Human-Machine Consensus: Visualized Dashboard Replaces Fragmented Operations

```
Traditional Fragmented Collaboration    Systematic Consensus Collaboration
─────────────────          ─────────────────
Fix issues one by one   →   AI proactively requests your feedback
                           on feature completion
                           ↓
Don't know what changed affected what →   Batch create improvement plans
                           Visualized dashboard display
                           ↓
Fixes introduce new bugs →   Refactoring automatically avoids
                           features you're satisfied with
                           ↓
Cannot form global cognition →   Human and machine achieve true consensus
```

**How?**
- Visualized dashboard displays global project status, enabling AI to reach consensus with you
- Batch generate improvement plans, proactively organize iteration cycles, rather than scattered issue-by-issue approach
![3_en](https://github.com/user-attachments/assets/668aff98-529c-4d8d-b1dc-4ce5c31ff92a)


- AI proactively requests your feedback on each feature's completion level (satisfied/needs improvement), automatically identifying and protecting features you're already satisfied with during refactoring
<img width="1344" height="768" alt="4_en" src="https://github.com/user-attachments/assets/7d895441-08ed-4e31-825f-df55552f29f1" />


- Proactively display systematic hypotheses and potential risks of current approach, avoiding complete overturn due to incorrect prerequisites
<img width="1344" height="768" alt="5_en" src="https://github.com/user-attachments/assets/5c32832f-c8db-4d82-9dbc-e4c3bb466f3a" />


- Other points you care about, freely configurable
---

## Skill System: Self-Composition and Self-Evolution

This skill system is not just four independent tools — they can **automatically combine** into more powerful system-level capabilities and **self-evolve**.

### Skill Self-Composition: 1+1>2

```
┌─────────────────────────────────────────────────────────┐
│              Skill Combination Examples                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   code-observer + dev-observability                     │
│   = Automatic code performance bottleneck identification │
│     + Project progress correlation analysis             │
│                                                         │
│   dev-observability + skill-evolution-driver            │
│   = Automatic project risk early warning                │
│     + Automatic skill optimization triggering           │
│                                                         │
│   code-observer + skill-evolution-driver                │
│   = Automatic code issue discovery                      │
│     + Skill self-repair suggestions                     │
│                                                         │
│   Four skills collaborating = Deterministic             │
│   collaboration closed loop                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Skill Self-Evolution: Growing With Your Project

Skills are not static tools — they **automatically analyze areas needing improvement** as the project progresses:

```
Project Initialization Phase        Project Iteration Phase        Project Maturity Phase
─────────────                ─────────────                ─────────────
Discover lack of progress   →     Automatically trigger    →   Accumulate project-specific
tracking functionality              adding test instrumentation    knowledge base and rule set
Automatically suggest                Automatically optimize             Self-evolution continues
enabling dev-observability          code analysis rules
```

**Private Knowledge Accumulation**:
- As skills self-grow, your project-specific knowledge (architecture decisions, performance baselines, error patterns) is also being deposited
- This knowledge becomes the basis for future skill decisions, making AI increasingly understand your project
<img width="1344" height="768" alt="6_en" src="https://github.com/user-attachments/assets/fd4148ab-956b-45a5-be20-4d84ca953e22" />


---

## Four Core Skills Overview

| Skill | Role | Core Value |
|------|------|------------|
| **skill-manager** | Unified Storage Service | Provides data storage and sharing capabilities for all skills; infrastructure for skill collaboration |
| **cox** | Development Observability Foundation | Project/application/test three-dimension transparency; real-time visibility of collaboration status |
| **code-observer** | Code Debugging Assistant | Tracks code execution paths, discovers performance bottlenecks, locates error root causes |
| **skill-evolution-driver** | Skill Evolution Driver | Automatically discovers skill optimization opportunities, executes safe updates, ensures continuous skill improvement |

### Collaboration Relationship Diagram

```
                    ┌─────────────────────┐
                    │ skill-evolution-    │
                    │     driver          │
                    │  (self-evolution)   │
                    └──────────┬──────────┘
                               │ Monitor & Optimize
                               ▼
┌──────────────────┐     ┌─────────────────────┐
│  code-observer   │────▶│  skill-manager      │
│  (code transparency)│     │  (unified data storage)│
└──────────────────┘     └──────────┬──────────┘
          Read                    ▲
┌──────────────────┐               │
│      cox         │───────────────┘
│  (collaboration transparency)│
└──────────────────┘
```

---

## Cross-Platform Compatibility

This skill system uses standardized skill format (YAML frontmatter + Markdown documentation), tested compatible with mainstream AI platform skill systems:

| Platform | Compatibility | Notes |
|----------|---------------|-------|
| **Claude Code** | Fully Compatible | Native development environment, recommended |
| **Coze** | Fully Compatible | Supports skill import and invocation |
| **Dify** | Compatible | May require minor frontmatter adjustments |
| **Other skill-supporting platforms** | Mostly Compatible | Platforms following standard format can use |

### Operating System Compatibility

- **Windows**: Full support (MSYS/Git Bash/WSL)
- **macOS**: Full support (native terminal)
- **Linux**: Full support (native terminal)

All Python scripts have been cross-platform path processing compatibility.

---

## How to Use

### Prerequisites

- AI platform supporting skills (Claude Code/Coze/Dify, etc.)
- Python 3.7+ (required for some skills)
- Flask 2.0+ (cox Web solution)

### Installation Steps

1. **Copy skill directories to platform's skill directory**
   - Claude Code: `~/.claude/skills/` or `.claude/skills/`
   - Coze: Import skill package through platform interface
   - Other platforms: Refer to respective platform's skill installation guide

2. **Restart AI platform to load skills**

---

## Detailed Usage Instructions for Each Skill

### cox - Development Observability Foundation

**Trigger Scenarios**:
- Project initialization, need to establish project monitoring
- Want to understand project progress, identify risks
- Complex or recurring issues arise, need systematic tracking

**Trigger Methods**:

| Trigger Category | Specific Trigger Words |
|-----------------|----------------------|
| **Core Concept Triggers** | "Transparency", "deterministic collaboration", "observe project status", "enable observation", "understand system health" |
| **Project Progress Queries** | "Want to know project progress", "any delay risks", "iteration completion percentage" |
| **Issue Tracking** | "How to track frequent bugs", "handle recurring issues", "need to record unresolved issues" |
| **Quality Assurance** | "Need to monitor API performance", "discover system anomalies", "test coverage status" |
| **Team Collaboration** | "Need to share project information", "let team understand status", "need visualization dashboard" |

**Typical Dialogue Example**:

```
You: Enable observation
AI: [cox triggered]
    Helping establish project observability. First, confirm a few questions:
    1. Your team size? (individual/small team/large team)
    2. What level of visualization? (simple log/Web interface/complete monitoring)
    ...
```

**Deployment Solution Selection**:
- **Simple Solution**: Generate structured logs only, suitable for individual development
- **Intermediate Solution**: Provide local Web interface, suitable for small teams (recommended)
- **Comprehensive Solution**: Prometheus+Grafana professional monitoring (coming soon)

---

### code-observer - Code Debugging Assistant

**Trigger Scenarios**:
- Code performance issues (too slow)
- Code execution errors, unsure where problem is
- Complex business logic, unclear execution order

**Trigger Methods**:

| Trigger Category | Specific Trigger Words |
|-----------------|----------------------|
| **Performance Issues** | "Code runs slow", "why is this function so slow", "where are performance bottlenecks" |
| **Error Troubleshooting** | "Code errors during execution", "don't know where the problem is", "locate bug" |
| **Logic Understanding** | "Business logic too complex", "can't clarify execution order", "want to see how code executes" |
| **Code Quality** | "Observe code execution", "code quality", "optimize code" |

**Typical Dialogue Example**:

```
You: Want to see why this function is so slow
AI: [code-observer triggered]
    Help trace code execution. First confirm debugging environment:
    1. Open application terminal (if not already open)
    2. Confirm cox logs are recording
    ...

    [After reading and analyzing logs]
    Found performance bottleneck: checkout() function accounts for 60% execution time
    Cause: Database query not using index
    Suggestion: [specific optimization plan]

    Additionally, during analysis discovered a skill optimization opportunity:
    cox log format lacks timestamp field
    Need to call skill-evolution-driver to handle this optimization?
```

**Important Features**:
- Automatically calls skill-manager to query data storage location
- When discovering skill optimization points, proactively asks whether to trigger skill-evolution-driver
- When dependency files are missing, forcibly records issues to skill-manager

---

### skill-evolution-driver - Skill Evolution Driver

**Trigger Scenarios**:
- You directly request skill optimization or improvement
- code-observer discovers skill issues and asks whether to optimize
- Periodic monitoring discovers skill optimization opportunities (auto-trigger reminder)

**Trigger Methods**:

| Trigger Category | Specific Trigger Words |
|-----------------|----------------------|
| **User Initiative** | "Optimize skills", "improve skills", "skills need update", "skill upgrade", "fix skill issues" |
| **Version Management** | "Skill version needs update", "need to record skill changes" |
| **Quality Check** | "Skill format incorrect", "need to check skill quality", "skill tests failing" |
| **Auto Trigger** | Pending optimization tasks, error logs, missing fields detected in skill-manager stored data |

**Typical Dialogue Example**:

```
You: Optimize skills
AI: [skill-evolution-driver triggered]
    [Check skill-manager stored data]

    Detected following optimization opportunities:

    1. Skill: cox
       - Optimization type: Script output optimization
       - Issue: observability.log file lacks timestamp field
       - Impact: Cannot track code execution path chronologically

    2. Skill: code-observer
       - Optimization type: Format improvement
       - Issue: SKILL.md lacks version field
       - Impact: Version management non-compliant

    Start optimization? (selective processing available)
```

**Evolution Process**:
1. Remind user of optimization opportunities
2. Maintain optimization task list (stored in skill-manager)
3. Analyze feasibility
4. Backup skill
5. Execute optimization and update version number
6. Test verification
7. If test passes, complete; if fails, auto-restore
8. Notify user of results

---

### skill-manager - Skill Manager

**Trigger Scenarios**: Automatically invoked by other skills like `cox`, `code-observer`, `skill-evolution-driver`

---

## One-Phrase Quick Triggers

```
Enable observation          # Start cox, establish project observability

Code runs slow             # Trigger code-observer, analyze performance bottlenecks

Optimize skills            # Trigger skill-evolution-driver, check and optimize skills

View skill data            # View all skill configs and logs stored by skill-manager
```

---

## Directory Structure

```
.claude/skills/
├── code-observer/          # Code debugging assistant
│   ├── SKILL.md
│   ├── scripts/            # Log parsing, report generation scripts
│   ├── references/         # Format specifications, analysis guides
│   └── assets/             # Tracing report templates
├── cox/                    # Development observability foundation
│   ├── SKILL.md
│   ├── scripts/            # Data collection, Web service scripts
│   ├── references/         # Data formats, deployment guides
│   └── assets/             # Web templates, Docker configs
├── skill-evolution-driver/ # Skill evolution driver
│   ├── SKILL.md
│   ├── scripts/            # Optimization check, backup & restore scripts
│   └── references/         # Optimization guides
├── skill-manager/          # Skill manager
│   ├── SKILL.md
│   ├── scripts/            # SkillStorage core module
│   └── references/         # API specifications
└── shared/                 # Shared utilities
    └── path_utils.py       # Path processing utilities
```

---

## Development Roadmap

- [ ] Enhance end-to-end collaboration capabilities for non-technical users
- [ ] Support custom tracing templates
- [ ] Enhance Web interface interactivity
- [ ] Explore more dimensions of human-machine collaboration capability extensions

---

## Contributing

Issues and Pull Requests are welcome!

---

## License

MIT License

---

## Contact

For questions or suggestions, please submit an Issue.
