"""Writer Agent - Creates and revises documents."""
from .base_agent import BaseAgent
from ..orchestrator.state import WorkflowState, ApprovalStatus, AgentApproval
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WriterAgent(BaseAgent):
    """
    Agent responsible for creating and revising documents.

    The Writer:
    - Creates initial drafts from prompts
    - Revises based on reviewer and human feedback
    - Can express approval when satisfied with the document
    """

    @property
    def name(self) -> str:
        return "WriterAgent"

    @property
    def system_prompt(self) -> str:
        return """You are a Data Science Principal and technical document author.
You have deep expertise in machine learning, statistical modeling, predictive analytics,
data engineering, and MLOps. You write for a technical audience of peer data scientists.

YOUR BACKGROUND:
- Expert in ML/AI: supervised/unsupervised learning, deep learning, NLP, time series
- Strong in statistics: hypothesis testing, Bayesian methods, experimental design
- Experienced with: Python, R, SQL, Spark, cloud ML platforms (AWS, GCP, Azure)
- Understand production ML: model deployment, monitoring, drift detection, A/B testing

WRITING GUIDELINES:
1. Write technically precise documents - use proper terminology
2. Include methodology details, assumptions, and limitations
3. Reference appropriate algorithms, metrics, and evaluation approaches
4. Structure documents with clear sections (Problem, Approach, Methods, Results, etc.)
5. Use equations, pseudocode, or diagrams (in markdown) when they add clarity
6. Be rigorous but accessible to fellow data scientists

OUTPUT FORMAT:
- Provide the complete document in markdown format
- End with "WRITER_APPROVED" if you believe the document is technically sound and complete
- Otherwise, note specific technical concerns or questions

You are collaborating with a peer Data Science Principal (reviewer) and a human stakeholder.
All three must approve before the document is finalized."""

    def process(self, state: WorkflowState) -> WorkflowState:
        """Create or revise the document based on current state."""
        if state.iteration == 0:
            # Initial creation
            prompt = f"""Please create a document based on the following requirements:

{state.document_prompt}

Write the complete document in markdown format."""
        else:
            # Revision based on feedback
            feedback_parts = []

            if state.reviewer_approval.feedback:
                feedback_parts.append(
                    f"REVIEWER FEEDBACK:\n{state.reviewer_approval.feedback}"
                )

            if state.human_approval.feedback:
                feedback_parts.append(
                    f"HUMAN FEEDBACK:\n{state.human_approval.feedback}"
                )

            combined_feedback = "\n\n".join(feedback_parts)

            prompt = f"""Please revise the document based on the following feedback:

{combined_feedback}

CURRENT DOCUMENT:
{state.current_document}

Provide the complete revised document in markdown format."""

        response = self.send_message(prompt)

        # Check for writer approval
        if "WRITER_APPROVED" in response.upper():
            state.writer_approval = AgentApproval(
                status=ApprovalStatus.APPROVED,
                feedback="Document meets requirements",
                timestamp=datetime.now()
            )
            # Remove approval marker from document
            response = response.replace("WRITER_APPROVED", "").replace("Writer_Approved", "").strip()
            logger.info("Writer has approved the document")
        else:
            state.writer_approval = AgentApproval(
                status=ApprovalStatus.PENDING,
                timestamp=datetime.now()
            )

        state.current_document = response
        state.writer_messages = self.conversation_history.copy()

        return state
