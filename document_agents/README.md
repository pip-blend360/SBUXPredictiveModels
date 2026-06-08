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
├── requirements.md            # Your document requirements
├── source_document.pdf        # Original document (if rewriting/expanding)
├── reference_material.pdf     # Supporting context
└── data_dictionary.csv        # Additional materials
```

See `background/example_requirements.md` for a template.

### 2. Run the System

**Using Claude Code:**
```bash
cd document_agents
# Then invoke the Writer Agent with your prompt
```

**Your prompt should:**
- Describe what document you want to create
- Reference files in the `background/` folder
- Specify any particular requirements

**Example prompts:**
- "Write a technical specification for a machine learning model based on requirements.md"
- "Rewrite original_spec.pdf to be more comprehensive, following the guidelines in rewrite_requirements.md"
- "Create a research proposal based on the papers in the background folder"

### 3. The Three-Agent Workflow

The system follows an iterative review cycle:

**Iteration Loop:**
1. **Writer Agent** creates/revises document → `output/document.md`
2. **Reviewer Agent** evaluates quality → adds feedback to `output/feedback.md`
3. **Human (You)** reviews the document and feedback
4. You add your feedback to `output/feedback.md`:
   - Provide specific comments, suggestions, corrections
   - The Writer will read your feedback and make revisions
5. Loop repeats until the document meets your standards

**When to stop:**
- When you're satisfied with the document quality
- When Reviewer gives `APPROVED` status and you agree
- Typically takes 2-4 iterations

### 4. Review Outputs

**Primary output:**
- `output/document.md` - Your final document

**Supporting files:**
- `output/feedback.md` - All review feedback (Reviewer + Human)
- `output/session_log.md` - Complete session activity log

### 5. Tips for Best Results

- **Be specific in your initial prompt** - clear requirements lead to better outputs
- **Provide context** - add relevant background materials to `background/`
- **Give detailed feedback** - the more specific you are, the better the revisions
- **Iterate as needed** - don't expect perfection on the first draft
- **Use the Reviewer's feedback** - they often catch issues you might miss

## How It Works

### Agent Roles

**Writer Agent** (`skills/writer.md`)
- Creates document drafts based on requirements
- Revises based on feedback from Reviewer and Human
- Expertise in technical writing, ML/data science, cloud platforms
- Outputs: `output/document.md`

**Reviewer Agent** (`skills/reviewer.md`)
- Provides independent technical peer review
- Evaluates: accuracy, completeness, clarity, feasibility
- Identifies Critical/Major/Minor issues
- Outputs: Feedback added to `output/feedback.md`

**Human (You)**
- Final authority on document quality
- Adds business context and domain expertise
- Approves or requests revisions
- Outputs: Feedback added to `output/feedback.md`

### Key Design Principles

1. **File-based communication** - Agents communicate through files, not conversation history
2. **Independent agents** - Each agent runs separately with fresh context
3. **Human-in-the-loop** - You control the quality bar and final approval
4. **Iterative refinement** - Multiple review cycles improve quality
5. **Full transparency** - All feedback and revisions are logged

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

## Use Cases

This system is ideal for:

**Technical Documentation:**
- API specifications
- System architecture documents
- Technical design documents
- Implementation guides

**Research & Analysis:**
- Research proposals
- Literature reviews
- Data analysis reports
- Methodology documents

**Business Documents:**
- Product requirements documents (PRDs)
- Strategy documents
- Project proposals
- Executive summaries

**Rewriting & Expansion:**
- Taking rough notes and creating polished documents
- Expanding brief specs into comprehensive documentation
- Rewriting existing documents with new structure/clarity

## AI-Agnostic Design

This system uses markdown-based agent prompts with no code dependencies. Works with:
- **Claude** (via Claude Code CLI, API, or Projects)
- **GPT-4** (via OpenAI API or ChatGPT)
- **Any LLM** that can read files and follow markdown instructions

The agents are just markdown files - you can customize them for any use case.

## Example Projects

**Included example:**
- `background/example_requirements.md` - Customer churn model specification

**Create your own:**
1. Add your materials to `background/`
2. Craft a clear initial prompt
3. Let the agents iterate to create your document

## Advanced Usage

**Customizing Agents:**
- Edit `skills/writer.md` to change Writer expertise or style
- Edit `skills/reviewer.md` to adjust review criteria
- Keep the file-based communication structure intact

**Multiple Documents:**
- Create separate folders for different projects
- Copy the entire `document_agents/` structure
- Run multiple projects independently

**Version Control:**
- Commit after each iteration to track changes
- Use git branches for different document versions
- Review history shows the evolution of the document
