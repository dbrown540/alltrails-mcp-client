"""
AllTrails MCP - Model Context Protocol server for AllTrails data.

This package provides:
- MCP server for Claude Desktop integration
- Scraper for AllTrails trail data
- CLI tools for searching trails
- Park slug constants and utilities
"""

__version__ = "0.1.0"
__author__ = "Srinath Srinivasan, Danny Brown"
__license__ = "MIT"

from alltrails_mcp.scraper import search_trails_in_park, get_trail_by_slug
from alltrails_mcp.parks import NationalPark, PARK_SLUGS, get_park_slug, list_parks
from alltrails_mcp.cache import TrailCache, search_trails_with_cache

__all__ = [
    "search_trails_in_park", 
    "get_trail_by_slug", 
    "NationalPark",
    "PARK_SLUGS",
    "get_park_slug",
    "list_parks",
    "TrailCache",
    "search_trails_with_cache",
    "__version__"
]
