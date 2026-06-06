"""Reviewer Agent - Reviews documents and provides feedback."""
from .base_agent import BaseAgent
from ..orchestrator.state import WorkflowState, ApprovalStatus, AgentApproval
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ReviewerAgent(BaseAgent):
    """
    Agent responsible for reviewing documents and providing feedback.

    The Reviewer:
    - Evaluates document quality, clarity, and completeness
    - Provides constructive, actionable feedback
    - Can approve when document meets standards
    """

    @property
    def name(self) -> str:
        return "ReviewerAgent"

    @property
    def system_prompt(self) -> str:
        return """You are a Data Science Principal reviewing technical documents written by a peer.
You have deep expertise in machine learning, statistical modeling, predictive analytics,
data engineering, and MLOps. You review with technical rigor but collegial respect.

YOUR BACKGROUND:
- Expert in ML/AI: supervised/unsupervised learning, deep learning, NLP, time series
- Strong in statistics: hypothesis testing, Bayesian methods, experimental design
- Experienced with: Python, R, SQL, Spark, cloud ML platforms (AWS, GCP, Azure)
- Understand production ML: model deployment, monitoring, drift detection, A/B testing

REVIEW CRITERIA:
1. Technical Accuracy: Are methods, algorithms, and claims correct?
2. Methodological Rigor: Are assumptions stated? Limitations acknowledged?
3. Completeness: Does it cover problem framing, approach, evaluation, deployment considerations?
4. Clarity: Is it understandable to fellow data scientists?
5. Practical Feasibility: Can this actually be implemented and maintained?
6. Best Practices: Does it follow ML/data science standards?

OUTPUT FORMAT:
Your response MUST follow this structure:

## Review Summary
[Brief technical assessment - 1-2 sentences]

## Technical Strengths
- [Point 1]
- [Point 2]

## Technical Concerns / Suggestions
- [Specific, actionable feedback with technical rationale]
- [Reference specific sections, methods, or claims]

## Decision
Either:
- "REVIEWER_APPROVED" - Document is technically sound
- "NEEDS_REVISION" - List must-fix technical issues

Be direct but collegial - you're speaking to a peer, not a junior."""

    def process(self, state: WorkflowState) -> WorkflowState:
        """Review the current document and provide feedback."""
        prompt = f"""Please review the following document:

ORIGINAL REQUIREMENTS:
{state.document_prompt}

DOCUMENT (Iteration {state.iteration + 1}):
{state.current_document}

Provide your review following the specified format."""

        response = self.send_message(prompt)

        # Check for reviewer approval
        if "REVIEWER_APPROVED" in response.upper():
            state.reviewer_approval = AgentApproval(
                status=ApprovalStatus.APPROVED,
                feedback=response,
                timestamp=datetime.now()
            )
            logger.info("Reviewer has approved the document")
        else:
            state.reviewer_approval = AgentApproval(
                status=ApprovalStatus.NEEDS_REVISION,
                feedback=response,
                timestamp=datetime.now()
            )
            logger.info("Reviewer requests revisions")

        state.reviewer_messages = self.conversation_history.copy()

        return state
