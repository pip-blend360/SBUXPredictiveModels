"""Entry point for the document writing system."""
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .orchestrator.orchestrator import Orchestrator
from .config import Config
from .utils.logging_config import setup_logging


def main():
    parser = argparse.ArgumentParser(
        description="Three-Agent Document Writing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main "Write a technical specification for a REST API"
  python -m src.main --prompt-file requirements.md
  python -m src.main --max-iterations 5 "Write a user guide"
        """
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Document prompt/requirements (or use --prompt-file)"
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        help="Path to file containing document prompt"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="Maximum iterations before timeout (default: 10)"
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-20250514",
        help="Claude model to use (default: claude-sonnet-4-20250514)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(verbose=args.verbose)

    # Get prompt
    if args.prompt_file:
        if not args.prompt_file.exists():
            print(f"Error: Prompt file not found: {args.prompt_file}")
            sys.exit(1)
        prompt = args.prompt_file.read_text(encoding="utf-8")
    elif args.prompt:
        prompt = args.prompt
    else:
        print("Error: Provide a prompt or --prompt-file")
        print("Use --help for usage information")
        sys.exit(1)

    # Configure and run
    config = Config(
        model=args.model,
        max_iterations=args.max_iterations
    )

    print("\n" + "=" * 60)
    print("THREE-AGENT DOCUMENT WRITING SYSTEM")
    print("=" * 60)
    print(f"Model: {config.model}")
    print(f"Max iterations: {config.max_iterations}")
    print(f"Output: {config.document_path}")
    print("=" * 60 + "\n")

    orchestrator = Orchestrator(config)
    state = orchestrator.run(prompt)

    # Exit code based on outcome
    if state.termination_reason == "CONSENSUS_REACHED":
        print("\nSuccess! Document has been approved by all parties.")
        sys.exit(0)
    else:
        print(f"\nWorkflow ended: {state.termination_reason}")
        sys.exit(1)


if __name__ == "__main__":
    main()
