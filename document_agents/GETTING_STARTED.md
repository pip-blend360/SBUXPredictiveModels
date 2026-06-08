# Getting Started Guide

This guide walks you through your first document creation session.

## Prerequisites

- Claude Code CLI installed (or another LLM tool)
- Basic familiarity with markdown
- Your source materials ready

## Step-by-Step Tutorial

### Step 1: Prepare Your Materials

```bash
cd document_agents/background/
```

Add your files:
- Source document (if rewriting/expanding)
- Requirements or specifications
- Any reference materials

**Example:**
```
background/
├── original_draft.md          # Your rough draft
├── requirements.md            # What you want in the final doc
└── reference_paper.pdf        # Supporting material
```

### Step 2: Write a Clear Initial Prompt

Your prompt should include:
1. **What you want** - Type of document (spec, proposal, guide, etc.)
2. **Source materials** - Reference files in `background/`
3. **Specific requirements** - Length, structure, audience, style

**Good prompt examples:**

```
"Write a comprehensive technical specification for the ML model described in
requirements.md. Use the data dictionary in data_dict.csv for feature definitions.
Target audience: data science team and engineering stakeholders."
```

```
"Rewrite original_draft.md into a polished executive summary. Make it concise
(2-3 pages), non-technical, and focus on business value. Use the ROI analysis
in financial_model.xlsx for metrics."
```

```
"Create a research proposal based on the papers in background/. Include:
literature review, research questions, methodology, timeline. Follow the
structure in proposal_template.md."
```

### Step 3: Invoke the Writer Agent

Using Claude Code:
```bash
cd document_agents
# Then interact with Claude Code and provide your prompt
```

The Writer Agent (using `skills/writer.md`) will:
- Read materials from `background/`
- Create initial draft in `output/document.md`
- Log activity in `output/session_log.md`

### Step 4: Review the Draft

Open `output/document.md` and review the initial draft.

**Common first-draft issues:**
- Missing details or context
- Wrong structure or emphasis
- Style doesn't match your needs
- Technical inaccuracies

Don't worry - this is expected! The iterative process will fix these.

### Step 5: Invoke the Reviewer Agent

The Reviewer Agent will:
- Read `output/document.md`
- Provide detailed technical feedback
- Add feedback to `output/feedback.md`
- Flag Critical, Major, and Minor issues

### Step 6: Add Your Human Feedback

Open `output/feedback.md` and add a new section:

```markdown
# Human - Iteration 1

**Human:** [Your Name]
**Date:** [Today's Date]

## Review

* [Your specific feedback item 1]
* [Your specific feedback item 2]
* [Your specific feedback item 3]

**HUMAN STATUS:** NEEDS REVISION
```

**Tips for good feedback:**
- Be specific: "Add a section on data validation" vs "needs more detail"
- Prioritize: Mark which items are critical vs nice-to-have
- Provide examples: Show what good looks like
- Reference sources: Point to specific background materials

### Step 7: Writer Revises

Invoke the Writer Agent again. They will:
- Read ALL feedback (Reviewer + Human)
- Make revisions to address comments
- Update `output/document.md`
- Log the changes

### Step 8: Iterate

Repeat Steps 5-7 until:
- Reviewer gives `APPROVED` status
- You're satisfied with the quality
- All critical issues are addressed

**Typical iteration count:** 2-4 cycles

### Step 9: Finalize

When done:
1. Review final `output/document.md`
2. Check `output/session_log.md` for complete history
3. Commit to git (preserves all versions)
4. Export to other formats if needed (Word, PDF, etc.)

## Tips for Success

### Write a Strong Initial Prompt

❌ **Weak:** "Write a document about machine learning"

✅ **Strong:** "Write a technical specification for a customer churn prediction model using the requirements in requirements.md and data from data_dict.csv. Target audience: ML engineers and data scientists. Include: model architecture, feature engineering, evaluation metrics, deployment plan."

### Provide Detailed Feedback

❌ **Weak:** "This needs improvement"

✅ **Strong:**
- "Add specific MAPE targets for the evaluation section (suggest ≤15%)"
- "The feature engineering section is missing seasonality handling"
- "Include code examples for the API integration section"

### Use Background Materials Effectively

The more context you provide, the better:
- Original documents to rewrite
- Requirements and specifications
- Data dictionaries and schemas
- Example documents for style reference
- Research papers for technical context

### Iterate Thoughtfully

- Don't expect perfection on draft 1
- Use the Reviewer's feedback - they catch issues
- Be willing to do 2-4 iterations
- Each cycle improves quality significantly

## Troubleshooting

**"Writer isn't addressing my feedback"**
- Make feedback more specific
- Provide examples of what you want
- Reference exact sections/line numbers

**"Document is too generic"**
- Add more specific background materials
- Provide domain-specific requirements
- Give concrete examples in your feedback

**"Reviewer is too picky"**
- This is by design - they set a high bar
- You can override their suggestions in your feedback
- Focus on Critical/Major issues first

**"Too many iterations"**
- Set clearer requirements upfront
- Provide more detailed initial prompt
- Consolidate feedback (don't give one item at a time)

## Next Steps

After your first successful document:
- Try different document types
- Customize the agent skills for your domain
- Create templates for your common use cases
- Share the system with your team

**Questions?** See the main README.md or review the example files in `background/`.
