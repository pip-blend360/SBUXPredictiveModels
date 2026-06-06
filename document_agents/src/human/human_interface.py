"""File-based human feedback interface."""
from pathlib import Path
from ..orchestrator.state import WorkflowState, ApprovalStatus, AgentApproval
from ..config import Config
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

FEEDBACK_TEMPLATE = """# Human Feedback for Document Review

## Instructions
This is iteration {iteration} of the review process.
After reviewing on GitHub, summarize your feedback here.

## Reviewer's Assessment
{reviewer_feedback}

## Your Feedback
Write your feedback below the line. When finished, SAVE THIS FILE.
- Type "APPROVED" on its own line if you approve the document
- Otherwise, provide specific feedback for revisions

---
YOUR FEEDBACK HERE:


"""


class HumanInterface:
    """
    Manages file-based human feedback collection.

    Workflow:
    1. Save current document to markdown file
    2. Create/update feedback file with template
    3. Wait for human to modify feedback file
    4. Parse feedback and determine approval status
    """

    def __init__(self, config: Config):
        self.config = config
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create output directories if they don't exist."""
        self.config.output_dir.mkdir(exist_ok=True)
        self.config.history_dir.mkdir(exist_ok=True)

    def save_document(self, state: WorkflowState) -> Path:
        """Save the current document to the output file."""
        self.config.document_path.write_text(
            state.current_document,
            encoding="utf-8"
        )

        # Also save to history
        history_path = self.config.history_dir / f"document_v{state.iteration + 1}.md"
        history_path.write_text(state.current_document, encoding="utf-8")

        logger.info(f"Document saved to: {self.config.document_path}")
        return self.config.document_path

    def prepare_feedback_file(self, state: WorkflowState) -> Path:
        """Create the feedback file with instructions and context."""
        content = FEEDBACK_TEMPLATE.format(
            document_path=self.config.document_path.absolute(),
            iteration=state.iteration + 1,
            reviewer_feedback=state.reviewer_approval.feedback or "No reviewer feedback yet"
        )

        self.config.feedback_path.write_text(content, encoding="utf-8")
        logger.info(f"Feedback template created: {self.config.feedback_path}")
        return self.config.feedback_path

    def prompt_push_to_github(self) -> None:
        """Prompt user to push changes to GitHub for review."""
        print("\n" + "=" * 60)
        print("PUSH TO GITHUB")
        print("=" * 60)
        print(f"Document ready: {self.config.document_path.absolute()}")
        print(f"Session log: {self.config.session_log_path.absolute()}")
        print("\nPlease push to GitHub now:")
        print("  git add .")
        print("  git commit -m \"Iteration update\"")
        print("  git push")
        print("\nReview the document on GitHub.")
        print("=" * 60)
        input("\nPress ENTER when you have pushed and are ready to review on GitHub...")

    def prompt_pull_from_github(self) -> None:
        """Prompt user to pull changes from GitHub after review."""
        print("\n" + "=" * 60)
        print("PULL FROM GITHUB")
        print("=" * 60)
        print("After reviewing on GitHub, pull any changes:")
        print("  git pull")
        print(f"\nThen edit your feedback file: {self.config.feedback_path.absolute()}")
        print("- Type 'APPROVED' if the document is ready")
        print("- Or provide your revision feedback")
        print("=" * 60)
        input("\nPress ENTER when you have pulled from GitHub...")

    def wait_for_feedback(self) -> str:
        """
        Wait for human to modify the feedback file.

        Detects changes by monitoring file modification time.
        """
        feedback_path = self.config.feedback_path
        initial_mtime = feedback_path.stat().st_mtime

        print("\n" + "-" * 60)
        print("WAITING FOR FEEDBACK")
        print("-" * 60)
        print(f"Feedback file: {feedback_path.absolute()}")
        print("\nEdit the feedback file and SAVE when done.")
        print("(Press Ctrl+C to abort)")
        print("-" * 60 + "\n")

        while True:
            time.sleep(self.config.feedback_poll_interval)

            current_mtime = feedback_path.stat().st_mtime
            if current_mtime > initial_mtime:
                content = feedback_path.read_text(encoding="utf-8")

                # Extract feedback after the separator line
                if "---" in content:
                    feedback = content.split("---", 1)[1].strip()
                    # Check if feedback was actually provided
                    if feedback and "YOUR FEEDBACK HERE:" not in feedback:
                        logger.info("Human feedback detected")
                        return feedback
                    # Remove the placeholder if present
                    feedback = feedback.replace("YOUR FEEDBACK HERE:", "").strip()
                    if feedback:
                        logger.info("Human feedback detected")
                        return feedback

                # File was modified but no valid feedback yet
                initial_mtime = current_mtime

    def parse_approval(self, feedback: str) -> AgentApproval:
        """Parse feedback text to determine approval status."""
        feedback_upper = feedback.upper()

        is_approved = any(
            keyword in feedback_upper
            for keyword in self.config.approval_keywords
        )

        if is_approved:
            logger.info("Human has approved the document")
            return AgentApproval(
                status=ApprovalStatus.APPROVED,
                feedback=feedback,
                timestamp=datetime.now()
            )
        else:
            logger.info("Human requests revisions")
            return AgentApproval(
                status=ApprovalStatus.NEEDS_REVISION,
                feedback=feedback,
                timestamp=datetime.now()
            )

    def process(self, state: WorkflowState) -> WorkflowState:
        """
        Full human feedback workflow with GitHub integration.

        1. Save document and prepare feedback file
        2. Prompt user to push to GitHub
        3. User reviews on GitHub
        4. Prompt user to pull from GitHub
        5. Wait for feedback file to be edited
        6. Parse and update state
        """
        self.save_document(state)
        self.prepare_feedback_file(state)

        # GitHub integration: push -> review on GitHub -> pull
        self.prompt_push_to_github()
        self.prompt_pull_from_github()

        feedback = self.wait_for_feedback()
        state.human_approval = self.parse_approval(feedback)

        return state
