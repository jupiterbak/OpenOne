#!/usr/bin/env python3
"""
Main entry point for AAC MCP Server using FastMCP.

This module provides a command-line interface to start the MCP server
with different transport options: stdio, SSE, or streamable HTTP.
"""

import argparse
import asyncio
import logging
import sys
from typing import Optional

from .server import AACMCPServer

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
        description="AAC MCP Server - Alteryx Analytics Cloud Model Context Protocol Server using FastMCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.aac_mcp                          # Start with stdio (default)
  python -m src.aac_mcp --transport stdio        # Start with stdio
  python -m src.aac_mcp --transport sse          # Start with SSE on localhost:8000
  python -m src.aac_mcp --transport sse --host 0.0.0.0 --port 9000
  python -m src.aac_mcp --transport streamable-http   # Start with streamable HTTP transport
  python -m src.aac_mcp --log-level DEBUG        # Enable debug logging
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
        version="AAC MCP Server 0.1.0 (FastMCP)"
    )
    
    return parser.parse_args()


async def main() -> None:
    """Main entry point."""
    args = parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    
    # Create the server instance
    try:
        server = AACMCPServer()
        logger.info(f"Created AAC MCP Server using FastMCP")
    except Exception as e:
        logger.error(f"Failed to create server: {e}")
        sys.exit(1)
    
    # Run the server with the specified transport
    try:
        if args.transport == "stdio":
            logger.info("Starting server with stdio transport")
            await server.run_stdio()
        elif args.transport == "sse":
            logger.info(f"Starting server with SSE transport on {args.host}:{args.port}")
            await server.run_sse(args.host, args.port)
        elif args.transport == "streamable-http":
            logger.info(f"Starting server with streamable HTTP transport on {args.host}:{args.port}")
            await server.run_streamable_http(args.host, args.port)
        else:
            logger.error(f"Unsupported transport: {args.transport}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


def run() -> None:
    """Synchronous entry point for console script."""
    asyncio.run(main())


if __name__ == "__main__":
    run()