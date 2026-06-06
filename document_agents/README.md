# Document Writing System

A simple three-agent system for collaborative technical document creation.

## Overview

Three independent agents work together:
- **Writer Agent**: Creates and revises documents
- **Reviewer Agent**: Provides technical peer review
- **Human (You)**: Final review and approval

## Quick Start

### 1. Add Background Materials

Place any reference materials in the `background/` folder:
```bash
background/
├── requirements.md
├── research_paper.pdf
├── data_dictionary.csv
└── ...
```

### 2. Run the Orchestrator

```bash
# Using Claude Code (or your LLM tool)
claude-code skills/orchestrator.md --prompt "Write a technical specification for a customer churn prediction model"
```

### 3. Workflow

The system will:
1. Writer creates initial draft → `output/document.md`
2. Reviewer evaluates → adds feedback to `output/feedback.md`
3. System prompts you to review
4. You edit `output/feedback.md`:
   - Add `**HUMAN STATUS: APPROVED**` if ready
   - Add `**HUMAN STATUS: NEEDS REVISION**` with feedback if not
5. Loop continues until all three approve

### 4. Review Output

Final document: `output/document.md`
Session log: `output/session_log.md`
Version history: `output/history/`

## Configuration

Edit `config.yaml` to customize:
- Max iterations
- Directory paths
- Approval keywords

## File Structure

```
document_agents/
├── skills/                  # Agent prompts
│   ├── orchestrator.md     # Main workflow
│   ├── writer.md           # Writer agent
│   ├── reviewer.md         # Reviewer agent
│   └── human_instructions.md
├── background/             # Your reference materials
├── output/                 # Generated files
│   ├── document.md
│   ├── feedback.md
│   ├── session_log.md
│   └── history/
├── config.yaml            # Configuration
└── README.md              # This file
```

## AI-Agnostic Design

This system uses markdown prompts and YAML config - no code dependencies. Works with:
- Claude (via Claude Code, API, or Projects)
- GPT-4 (via OpenAI API)
- Any LLM that can read files and follow markdown instructions

## Notes

- Each agent runs independently (no shared conversation state)
- Agents communicate through files in `output/`
- All three parties must approve for completion
- System maintains full session history and version control
