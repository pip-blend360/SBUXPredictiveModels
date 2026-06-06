"""Main orchestration logic for the multi-agent workflow."""
from anthropic import Anthropic
from ..agents.writer_agent import WriterAgent
from ..agents.reviewer_agent import ReviewerAgent
from ..human.human_interface import HumanInterface
from .state import WorkflowState, ApprovalStatus
from ..config import Config
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Manages the iterative document creation and review workflow.

    Workflow Loop:
    1. Writer creates/revises document
    2. Reviewer evaluates document
    3. Human provides feedback
    4. Check for consensus (all approve)
    5. If not consensus, loop back to Writer

    Termination conditions:
    - All three parties approve (success)
    - Maximum iterations reached (timeout)
    - User interrupts (Ctrl+C)
    - Unrecoverable error
    """

    def __init__(self, config: Config = None):
        self.config = config or Config.from_env()

        # Initialize Anthropic client (uses ANTHROPIC_API_KEY env var)
        self.client = Anthropic()

        # Initialize agents
        self.writer = WriterAgent(
            client=self.client,
            model=self.config.model,
            max_tokens=self.config.max_tokens
        )
        self.reviewer = ReviewerAgent(
            client=self.client,
            model=self.config.model,
            max_tokens=self.config.max_tokens
        )
        self.human = HumanInterface(self.config)

    def _init_session_log(self, prompt: str) -> None:
        """Initialize the session log file with header and prompt."""
        self.config.output_dir.mkdir(exist_ok=True)

        header = f"""# Document Writing Session Log

**Started:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Original Prompt/Requirements

{prompt}

---

## Session Activity

"""
        self.config.session_log_path.write_text(header, encoding="utf-8")

    def _log_activity(self, actor: str, iteration: int, summary: str, details: str = None) -> None:
        """Append an activity entry to the session log."""
        timestamp = datetime.now().strftime("%H:%M:%S")

        entry = f"""### Iteration {iteration} - {actor}
**Time:** {timestamp}

**Summary:** {summary}

"""
        if details:
            entry += f"""<details>
<summary>Details</summary>

{details}

</details>

"""
        entry += "---\n\n"

        with open(self.config.session_log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    def run(self, prompt: str) -> WorkflowState:
        """
        Execute the main orchestration loop.

        Args:
            prompt: The document creation prompt/requirements

        Returns:
            Final WorkflowState with completed document or termination reason
        """
        state = WorkflowState(document_prompt=prompt)

        # Initialize the session log
        self._init_session_log(prompt)

        logger.info("=" * 60)
        logger.info("Starting Document Writing Workflow")
        logger.info(f"Max iterations: {self.config.max_iterations}")
        logger.info("=" * 60)

        try:
            while not state.is_complete:
                state = self._run_iteration(state)

                # Check termination conditions
                if state.all_approved():
                    state.is_complete = True
                    state.termination_reason = "CONSENSUS_REACHED"
                    logger.info("All parties approved! Document complete.")

                elif state.iteration >= self.config.max_iterations:
                    state.is_complete = True
                    state.termination_reason = "MAX_ITERATIONS_REACHED"
                    logger.warning(f"Max iterations ({self.config.max_iterations}) reached")

                else:
                    # Continue to next iteration
                    state.save_version()
                    logger.info(f"Iteration {state.iteration} complete. Continuing...")

        except KeyboardInterrupt:
            state.is_complete = True
            state.termination_reason = "USER_INTERRUPTED"
            logger.info("Workflow interrupted by user")

        except Exception as e:
            state.is_complete = True
            state.termination_reason = f"ERROR: {str(e)}"
            logger.error(f"Workflow error: {e}", exc_info=True)

        self._print_summary(state)
        return state

    def _run_iteration(self, state: WorkflowState) -> WorkflowState:
        """Execute a single iteration of the workflow."""
        logger.info(f"\n--- Iteration {state.iteration + 1} ---")

        iteration_num = state.iteration + 1

        # Step 1: Writer creates/revises
        logger.info("Step 1: Writer processing...")
        state = self.writer.process(state)

        # Log writer activity
        writer_action = "Created initial draft" if state.iteration == 0 else "Revised document based on feedback"
        writer_status = "APPROVED" if state.writer_approval.status == ApprovalStatus.APPROVED else "Submitted for review"
        self._log_activity(
            actor="Writer (Data Science Principal)",
            iteration=iteration_num,
            summary=f"{writer_action}. Status: {writer_status}",
            details=f"Document length: {len(state.current_document)} characters"
        )

        # Step 2: Reviewer evaluates
        logger.info("Step 2: Reviewer processing...")
        state = self.reviewer.process(state)

        # Log reviewer activity
        reviewer_status = "APPROVED" if state.reviewer_approval.status == ApprovalStatus.APPROVED else "Requested revisions"
        self._log_activity(
            actor="Reviewer (Data Science Principal)",
            iteration=iteration_num,
            summary=f"Reviewed document. Decision: {reviewer_status}",
            details=state.reviewer_approval.feedback
        )

        # Step 3: Human feedback
        logger.info("Step 3: Awaiting human feedback...")
        state = self.human.process(state)

        # Log human activity
        human_status = "APPROVED" if state.human_approval.status == ApprovalStatus.APPROVED else "Requested revisions"
        self._log_activity(
            actor="Human",
            iteration=iteration_num,
            summary=f"Reviewed document. Decision: {human_status}",
            details=state.human_approval.feedback
        )

        # Step 4: Check if revision needed
        needs_revision = (
            state.reviewer_approval.status == ApprovalStatus.NEEDS_REVISION or
            state.human_approval.status == ApprovalStatus.NEEDS_REVISION
        )

        if needs_revision:
            # Writer needs to see latest feedback for next iteration
            # Approvals will be evaluated fresh after revision
            state.writer_approval.status = ApprovalStatus.PENDING
            logger.info("Revision requested - preparing next iteration")

        return state

    def _print_summary(self, state: WorkflowState) -> None:
        """Print workflow completion summary."""
        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETE")
        print("=" * 60)
        print(f"Iterations: {state.iteration + 1}")
        print(f"Termination: {state.termination_reason}")
        print(f"Writer Approved: {state.writer_approval.status.value}")
        print(f"Reviewer Approved: {state.reviewer_approval.status.value}")
        print(f"Human Approved: {state.human_approval.status.value}")
        print(f"Document saved to: {self.config.document_path}")
        print(f"Session log: {self.config.session_log_path}")
        print("=" * 60)

        # Log final outcome to session log
        final_entry = f"""## Session Complete

**Ended:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Iterations:** {state.iteration + 1}
**Outcome:** {state.termination_reason}

| Party | Final Status |
|-------|--------------|
| Writer | {state.writer_approval.status.value} |
| Reviewer | {state.reviewer_approval.status.value} |
| Human | {state.human_approval.status.value} |
"""
        with open(self.config.session_log_path, "a", encoding="utf-8") as f:
            f.write(final_entry)
