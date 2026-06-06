"""Workflow state management."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime


class ApprovalStatus(Enum):
    """Status of approval from each party."""
    PENDING = "pending"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"


@dataclass
class AgentApproval:
    """Tracks approval status for a single agent."""
    status: ApprovalStatus = ApprovalStatus.PENDING
    feedback: Optional[str] = None
    timestamp: Optional[datetime] = None


@dataclass
class WorkflowState:
    """
    Central state object tracking the entire workflow.

    This is the single source of truth passed through the orchestration loop.
    """
    # Document content
    current_document: str = ""
    document_prompt: str = ""

    # Version tracking
    iteration: int = 0
    version_history: list = field(default_factory=list)

    # Approval tracking (all three must approve)
    writer_approval: AgentApproval = field(default_factory=AgentApproval)
    reviewer_approval: AgentApproval = field(default_factory=AgentApproval)
    human_approval: AgentApproval = field(default_factory=AgentApproval)

    # Conversation history for context
    writer_messages: list = field(default_factory=list)
    reviewer_messages: list = field(default_factory=list)

    # Workflow status
    is_complete: bool = False
    termination_reason: Optional[str] = None

    def all_approved(self) -> bool:
        """Check if all three parties have approved."""
        return (
            self.writer_approval.status == ApprovalStatus.APPROVED and
            self.reviewer_approval.status == ApprovalStatus.APPROVED and
            self.human_approval.status == ApprovalStatus.APPROVED
        )

    def reset_approvals(self) -> None:
        """Reset all approvals when document is revised."""
        self.writer_approval = AgentApproval()
        self.reviewer_approval = AgentApproval()
        self.human_approval = AgentApproval()

    def save_version(self) -> None:
        """Save current document to version history."""
        self.version_history.append(self.current_document)
        self.iteration += 1
