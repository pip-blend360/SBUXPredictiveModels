# Document Writing Orchestrator

You are orchestrating a three-agent document writing workflow.

## Workflow

1. **Load configuration** from `config.yaml`
2. **Initialize session** - create output directory, start session log
3. **Run Writer agent** - creates or revises document
4. **Run Reviewer agent** - provides technical feedback
5. **Wait for Human** - pause for human to edit feedback.md
6. **Check consensus**:
   - If all three approve (WRITER APPROVED + REVIEWER APPROVED + HUMAN APPROVED) → COMPLETE
   - Else → loop back to step 3
7. **Max iterations check** - if reached max, stop with timeout status

## Configuration

Read from `config.yaml`:
- `max_iterations`: Maximum revision cycles (default: 10)
- `initial_prompt`: The document requirements
- `background_dir`: Path to background materials (default: background/)
- `output_dir`: Path for outputs (default: output/)

## Session Log

Maintain `output/session_log.md` with:
- Start time
- Original prompt
- Each iteration's activity (Writer, Reviewer, Human decisions)
- Final outcome

## Agent Execution

For each agent:
- Load the appropriate skill markdown (`skills/writer.md`, `skills/reviewer.md`)
- Replace template variables: {prompt}, {iteration}, {read: filepath}
- Execute with current LLM
- Save outputs to output/

## Human Interaction

After Reviewer completes:
1. Display message to user with instructions (from `skills/human_instructions.md`)
2. Wait for user to edit `output/feedback.md`
3. Detect when file is modified (poll every 5 seconds)
4. Read and parse human decision (APPROVED or NEEDS REVISION)

## Completion

When all approve or max iterations reached:
- Update session log with final status
- Save final document version to `output/history/document_final.md`
- Display summary to user

## Error Handling

- If background/ folder doesn't exist → create it with a README
- If output/ folder doesn't exist → create it
- If a skill file is missing → error with clear message
- If config.yaml is missing → use defaults
