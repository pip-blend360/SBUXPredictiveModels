# SBUXPredictiveModels
Plan and build the predictive models for Starbucks

## Project Structure

```
SBUXPredictiveModels/
├── document_agents/     # AI-powered document writing system
│   └── README.md       # See here for usage instructions
├── background/          # Project background materials
│   ├── Customer States June 2 alignment meeting.pptx
│   └── Customer States Predictive Models - framework and solution.docx
└── README.md           # This file
```

## Document Writing System

This project includes an AI-powered collaborative document writing system located in `document_agents/`.

The system uses three independent agents (Writer, Reviewer, Human) to create high-quality technical documents through an iterative review process.

**Key Features:**
- AI-agnostic (works with Claude, GPT-4, or any LLM)
- Markdown-based skills (no code required)
- File-based communication
- Human-in-the-loop review

**Quick Start:**
```bash
cd document_agents
# Add your materials to background/
# Run the orchestrator with your prompt
```

See [`document_agents/README.md`](document_agents/README.md) for detailed instructions.

## Background Materials

The `background/` folder contains project context and requirements:
- Customer states framework presentations
- Predictive model solution documentation
- Reference materials for the AI agents
