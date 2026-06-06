# Human Review Instructions

## Your Role

You are the final reviewer in the document writing process. The AI agents (Writer and Reviewer) have done their work, and now you need to provide your input.

## Review Process

1. **Read the document**: `output/document.md`
2. **Read the AI reviewer's feedback**: `output/feedback.md`
3. **Review background materials**: Check `background/` folder for context
4. **Provide your feedback**:

### If You Approve

Edit `output/feedback.md` and add at the end:

```markdown
---

## Human Review

**HUMAN STATUS: APPROVED**

Document is ready for publication.
```

### If You Want Revisions

Edit `output/feedback.md` and add at the end:

```markdown
---

## Human Review

**HUMAN STATUS: NEEDS REVISION**

Please address the following:

- [Your specific feedback point 1]
- [Your specific feedback point 2]
- [...]
```

## Notes

- Be specific in your feedback
- Reference specific sections or content
- The Writer agent will see your feedback in the next iteration
- All three parties (Writer, Reviewer, Human) must approve for the document to be complete
