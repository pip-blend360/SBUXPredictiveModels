# Three-Agent Document Writing System

A collaborative document writing system with three participants:
- **Writer Agent** - Data Science Principal who creates and revises technical documents
- **Reviewer Agent** - Data Science Principal who reviews and provides technical feedback
- **Human (You)** - Reviews on GitHub and provides final feedback

All three must approve before a document is finalized.

## Setup

1. **Install dependencies:**
   ```bash
   cd document_agents
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   # Option 1: Environment variable
   export ANTHROPIC_API_KEY=your-key-here

   # Option 2: Create .env file
   cp .env.example .env
   # Edit .env with your API key
   ```

## Usage

```bash
# With inline prompt
python -m src.main "Write a technical specification for a customer churn prediction model"

# With prompt file
python -m src.main --prompt-file requirements.md

# With options
python -m src.main --max-iterations 5 --verbose "Write a model evaluation framework"
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `prompt` | - | Document requirements (positional arg) |
| `--prompt-file` | - | Path to file containing requirements |
| `--max-iterations` | 10 | Max revision cycles before timeout |
| `--model` | claude-sonnet-4-20250514 | Claude model to use |
| `--verbose`, `-v` | false | Enable detailed logging |

## Workflow

The system follows this loop until all three parties approve:

```
Writer → Reviewer → [Push to GitHub] → [Review on GitHub] → [Pull] → Writer → ...
```

### Step-by-Step

#### 1. Writer Creates/Revises Document
The Writer agent creates an initial draft or revises based on feedback.

#### 2. Reviewer Evaluates
The Reviewer agent provides technical feedback on methodology, accuracy, and completeness.

#### 3. Push to GitHub
You'll see this prompt:
```
============================================================
PUSH TO GITHUB
============================================================
Document ready: C:\...\output\document.md
Session log: C:\...\output\session_log.md

Please push to GitHub now:
  git add .
  git commit -m "Iteration update"
  git push

Review the document on GitHub.
============================================================

Press ENTER when you have pushed and are ready to review on GitHub...
```

#### 4. Review on GitHub
Review the document on GitHub. Add comments, suggest changes, etc.

#### 5. Pull from GitHub
After reviewing, you'll see:
```
============================================================
PULL FROM GITHUB
============================================================
After reviewing on GitHub, pull any changes:
  git pull

Then edit your feedback file: C:\...\output\feedback.md
- Type 'APPROVED' if the document is ready
- Or provide your revision feedback
============================================================

Press ENTER when you have pulled from GitHub...
```

#### 6. Provide Feedback
Edit `output/feedback.md`:
- Type `APPROVED` if the document is ready
- Otherwise, write your revision feedback

Save the file and the system continues.

#### 7. Loop or Complete
- If all three approve → Document finalized
- Otherwise → Writer revises and the loop continues

## Output Files

| File | Description |
|------|-------------|
| `output/document.md` | Current document version |
| `output/feedback.md` | Your feedback file |
| `output/session_log.md` | Running log of all activity |
| `output/history/document_v1.md` | Version history |
| `logs/session_*.log` | Detailed debug logs |

## Session Log

The system maintains a markdown log (`output/session_log.md`) showing what each participant did:

```markdown
# Document Writing Session Log
**Started:** 2024-01-15 14:30:00

## Original Prompt/Requirements
[your prompt]

## Session Activity

### Iteration 1 - Writer (Data Science Principal)
**Time:** 14:30:15
**Summary:** Created initial draft. Status: Submitted for review

### Iteration 1 - Reviewer (Data Science Principal)
**Time:** 14:30:45
**Summary:** Reviewed document. Decision: Requested revisions

### Iteration 1 - Human
**Time:** 14:35:00
**Summary:** Reviewed document. Decision: Requested revisions

...

## Session Complete
**Outcome:** CONSENSUS_REACHED
```

## Approval Keywords

The system recognizes these as approval (case-insensitive):
- `APPROVED`
- `APPROVE`
- `LGTM`
- `ACCEPTED`
