import argparse
import sys

from ingest import ingest
from query import ask


def print_sources(sources):
    """Print source document references."""
    if not sources:
        return
    print("\n--- Sources ---")
    seen = set()
    for doc in sources:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "?")
        key = f"{source}:p{page}"
        if key not in seen:
            seen.add(key)
            print(f"  - {source} (page {page})")


def interactive_query():
    """Run an interactive query loop."""
    print("RAG Assistant - Interactive Mode")
    print("Type 'quit' or 'exit' to stop.\n")
    while True:
        try:
            question = input("Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if not question or question.lower() in ("quit", "exit"):
            print("Goodbye.")
            break
        answer, sources = ask(question)
        print(f"\nAnswer: {answer}")
        print_sources(sources)
        print()


def main():
    parser = argparse.ArgumentParser(description="RAG Assistant - PDF Q&A with Claude")
    subparsers = parser.add_subparsers(dest="command")

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest PDF documents")
    ingest_parser.add_argument(
        "--dir", default="docs", help="Directory containing PDF files (default: docs)"
    )

    # Query command
    query_parser = subparsers.add_parser("query", help="Ask a question")
    query_parser.add_argument(
        "question", nargs="?", default=None, help="Question to ask (omit for interactive mode)"
    )

    args = parser.parse_args()

    if args.command == "ingest":
        ingest(args.dir)
    elif args.command == "query":
        if args.question:
            answer, sources = ask(args.question)
            print(f"\nAnswer: {answer}")
            print_sources(sources)
        else:
            interactive_query()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
