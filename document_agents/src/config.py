"""Configuration constants and settings."""
from pathlib import Path
from dataclasses import dataclass, field
import os


@dataclass
class Config:
    """Application configuration."""

    # API Settings
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096

    # File Paths (relative to project root)
    output_dir: Path = field(default_factory=lambda: Path("output"))
    document_path: Path = field(default_factory=lambda: Path("output/document.md"))
    feedback_path: Path = field(default_factory=lambda: Path("output/feedback.md"))
    history_dir: Path = field(default_factory=lambda: Path("output/history"))
    session_log_path: Path = field(default_factory=lambda: Path("output/session_log.md"))

    # Workflow Settings
    max_iterations: int = 10
    feedback_poll_interval: int = 5  # seconds

    # Approval Keywords (case-insensitive)
    approval_keywords: tuple = ("APPROVED", "LGTM", "APPROVE", "ACCEPTED")

    def __post_init__(self):
        """Convert string paths to Path objects if needed."""
        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)
        if isinstance(self.document_path, str):
            self.document_path = Path(self.document_path)
        if isinstance(self.feedback_path, str):
            self.feedback_path = Path(self.feedback_path)
        if isinstance(self.history_dir, str):
            self.history_dir = Path(self.history_dir)
        if isinstance(self.session_log_path, str):
            self.session_log_path = Path(self.session_log_path)

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514"),
            max_iterations=int(os.getenv("MAX_ITERATIONS", "10")),
        )
