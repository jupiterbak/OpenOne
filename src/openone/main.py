#!/usr/bin/env python3
"""
Main entry point for OpenOne MCP Server using FastMCP.

This module provides a command-line interface to start the MCP server
with different transport options: stdio, SSE, or streamable HTTP.
"""
import click
import argparse
import asyncio
import logging
import sys
from typing import Optional

from .server import OpenOneMCPServer

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="OpenOne MCP Server - OpenOne Analytics Platform Model Context Protocol Server using FastMCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.openone                          # Start with stdio (default)
  python -m src.openone --transport stdio        # Start with stdio
  python -m src.openone --transport sse          # Start with SSE on localhost:8000
  python -m src.openone --transport sse --host 0.0.0.0 --port 9000
  python -m src.openone --transport streamable-http   # Start with streamable HTTP transport
  python -m src.openone --log-level DEBUG        # Enable debug logging
        """
    )
    
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport method to use (default: stdio)"
    )
    
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind to for SSE/streamable transports (default: localhost)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to for SSE/streamable transports (default: 8000)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="OpenOne MCP Server 0.1.0 (FastMCP)"
    )
    
    return parser.parse_args()

def main() -> None:
    """Main entry point."""
    args = parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    
    # Create the server instance
    try:
        server = OpenOneMCPServer()
        logger.info(f"Created OpenOne MCP Server using FastMCP")
    except Exception as e:
        logger.error(f"Failed to create server: {e}")
        sys.exit(1)
    
    # Run the server with the specified transport
    match args.transport:
        case "stdio":
            server.app.run(transport="stdio")
        case "sse":
            server.app.run(transport="sse", host=args.host, port=args.port, show_banner=False)
        case "streamable-http":
            server.app.run(transport="streamable-http", host=args.host, port=args.port, show_banner=False)


def run() -> None:
    """Synchronous entry point for console script."""
    main()


if __name__ == "__main__":
    run()
