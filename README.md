# Document Writing System

An AI-powered collaborative document creation system using three independent agents.

## Overview

This system helps you create high-quality technical documents through an iterative review process involving three agents:

- **Writer Agent**: Creates and revises documents
- **Reviewer Agent**: Provides technical peer review
- **Human (You)**: Final review and approval

## Key Features

- ✅ **AI-agnostic** - Works with Claude, GPT-4, or any LLM
- ✅ **Markdown-based** - No code required, just markdown prompts
- ✅ **File-based communication** - Agents communicate through files
- ✅ **Human-in-the-loop** - You control quality and final approval
- ✅ **Iterative refinement** - Multiple review cycles improve quality
- ✅ **Full transparency** - All feedback and revisions are logged

## Quick Start

```bash
cd document_agents

# 1. Add your materials to background/
# 2. Invoke the Writer Agent with your prompt
# 3. Review and iterate until document is approved
```

See [`document_agents/README.md`](document_agents/README.md) for complete instructions.

Or jump straight to [`document_agents/GETTING_STARTED.md`](document_agents/GETTING_STARTED.md) for a step-by-step tutorial.

## Project Structure

```
document_agents/
├── skills/                      # Agent prompts (markdown files)
│   ├── writer.md               # Writer agent prompt
│   ├── reviewer.md             # Reviewer agent prompt
│   └── orchestrator.md         # Workflow orchestration
├── background/                  # Your source materials go here
│   ├── example_requirements.md # Example template
│   └── README.md               # Instructions
├── output/                      # Generated documents
│   ├── document.md             # Your final document
│   ├── feedback.md             # Review feedback
│   └── session_log.md          # Activity log
├── README.md                   # System documentation
└── GETTING_STARTED.md          # Tutorial guide
```

## Use Cases

Perfect for creating:

- **Technical Documentation**: API specs, architecture docs, design docs
- **Research Documents**: Proposals, literature reviews, methodology docs
- **Business Documents**: PRDs, strategy docs, project proposals
- **Rewriting Projects**: Polish rough drafts, expand brief specs

## How It Works

1. **You** provide requirements and source materials
2. **Writer** creates initial draft based on your requirements
3. **Reviewer** evaluates quality and provides detailed feedback
4. **You** review and add your own feedback
5. **Writer** revises based on all feedback
6. Repeat until approved by all three agents

## Requirements

- An LLM tool that can read files and follow markdown instructions:
  - Claude Code CLI (recommended)
  - Claude API or Projects
  - GPT-4 via OpenAI API
  - Any compatible LLM tool

## Documentation

- **[document_agents/README.md](document_agents/README.md)** - Complete system documentation
- **[document_agents/GETTING_STARTED.md](document_agents/GETTING_STARTED.md)** - Step-by-step tutorial
- **[document_agents/background/example_requirements.md](document_agents/background/example_requirements.md)** - Example template

## License

MIT License - feel free to use and customize for your needs.
