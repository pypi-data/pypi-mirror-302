"""This handles the command-line interface (CLI) for the ETL (Extract, Transform, Load) process and querying."""

import sys
import argparse
from mylib.extract import extract
from mylib.transform_load import load
from mylib.query import query


def handle_arguments(args):
    """Add action based on initial calls"""
    parser = argparse.ArgumentParser(description="ETL-Query script")
    parser.add_argument(
        "action",
        choices=["extract", "load", "query"],
    )
    parser.add_argument(
        "--query-name",
        help="Name of the query to execute (required if action is 'query')",
        required=False,
    )
    parsed_args = parser.parse_args(args)
    return parsed_args


def main():
    """Handles all the CLI commands"""
    args = handle_arguments(sys.argv[1:])

    if args.action == "extract":
        extract()
    elif args.action == "load":
        load()
    elif args.action == "query":
        if not args.query_name:
            print("Please provide a query name using '--query-name' argument.")
            sys.exit(1)
        query(args.query_name)
    else:
        print(f"Unknown action: {args.action}")


if __name__ == "__main__":
    main()
