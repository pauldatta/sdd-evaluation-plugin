# SDD Evaluation Plugin for Antigravity

An **Antigravity / Gemini Agent Plugin** for evaluating Software Design Documents (SDDs) against architectural rigor, technical completeness, non-functional requirements, and implementation readiness.

---

## 📦 Directory Structure

```
sdd-evaluation-plugin/
├── plugin.json       # Plugin manifest file
├── README.md         # Documentation & installation guide
└── skills/
    └── sdd-evaluation/
        ├── SKILL.md
        └── references/
            ├── sdd-rubric.md
            └── sdd-template.md
```

---

## 🚀 How to Add This Plugin to Antigravity

Antigravity automatically discovers and loads plugins from designated workspace or global directories.

### Option 1: Global Level (All Workspaces)
Clone this repository directly into your user home directory's plugin folder:

```bash
git clone https://github.com/pauldatta/sdd-evaluation-plugin.git ~/.gemini/config/plugins/sdd-evaluation-plugin
```

### Option 2: Workspace Level (Current Project Only)
Clone this repository into your project's opened workspace directory:

```bash
# Inside your project root:
mkdir -p .agents/plugins
git clone https://github.com/pauldatta/sdd-evaluation-plugin.git .agents/plugins/sdd-evaluation-plugin
```

---

## 🎯 How to Use

Once installed, your Antigravity agent will automatically discover the `sdd-evaluation` skill. You can ask your agent:

* *"Evaluate my solution design document draft against the SDD rubric."*
* *"Perform an intake and gap analysis on my design doc in `docs/sdd.md`."*
* *"Grade my hackathon submission design doc across the 6 dimensions."*

---

## 📄 License & Ownership

Created by Paul Datta (`pkdatta2000@gmail.com`).
Free for all hackathon participants, solution architects, and engineering teams for self-assessing design documents before implementation.
