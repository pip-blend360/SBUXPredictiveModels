"""Abstract base class for AI agents."""
from abc import ABC, abstractmethod
from anthropic import Anthropic
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class defining the agent interface.

    All agents share common API interaction patterns but have
    different system prompts and behaviors.
    """

    def __init__(
        self,
        client: Anthropic,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096
    ):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.conversation_history: list = []

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the agent's name for logging."""
        pass

    def send_message(self, content: str) -> str:
        """
        Send a message to Claude and get a response.

        Maintains conversation history for multi-turn context.
        """
        self.conversation_history.append({
            "role": "user",
            "content": content
        })

        logger.info(f"{self.name}: Sending message to Claude...")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        logger.info(f"{self.name}: Received response ({len(assistant_message)} chars)")
        return assistant_message

    def reset_conversation(self) -> None:
        """Clear conversation history for a fresh start."""
        self.conversation_history = []

    @abstractmethod
    def process(self, state):
        """
        Process the current state and return updated state.

        Each agent implements its specific logic here.
        """
        pass
