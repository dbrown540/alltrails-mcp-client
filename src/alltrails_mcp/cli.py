#!/usr/bin/env python3
"""
Command-line interface for the AllTrails MCP package.
Allows direct searching and querying of trails without the MCP server.
"""

import sys
import argparse
import logging

from alltrails_mcp.scraper import search_trails_in_park, get_trail_by_slug
from alltrails_mcp.cache import TrailCache, search_trails_with_cache


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def search_command(args):
    """Handle the search command."""
    print(f"\n{'='*80}")
    print(f"Searching for trails in: {args.park}")
    if not args.no_cache:
        print("Using cache (use --no-cache to bypass)")
    print(f"{'='*80}\n")
    
    # Use cache by default unless --no-cache is specified
    if args.no_cache:
        trails = search_trails_in_park(args.park)
    else:
        cache = TrailCache()
        trails = search_trails_with_cache(
            args.park, 
            cache=cache, 
            force_refresh=args.force_refresh,
            limit=15
        )
    
    if not trails:
        print("❌ No trails found. Please check the park slug format.")
        print("   Format: 'us/state/park-name' (e.g., 'us/tennessee/great-smoky-mountains-national-park')")
        return 1
    
    print(f"✅ Found {len(trails)} trails!\n")
    
    # Display trails
    limit = args.limit or len(trails)
    for i, trail in enumerate(trails[:limit], 1):
        print(f"{i}. {trail['name']}")
        if trail.get('difficulty'):
            print(f"   Difficulty: {trail['difficulty']}")
        if trail.get('length'):
            print(f"   Length: {trail['length']}")
        if trail.get('rating'):
            print(f"   Rating: {trail['rating']}")
        if args.show_urls:
            print(f"   URL: {trail['url']}")
        if args.show_summary and trail.get('summary'):
            summary = trail['summary'][:100] + "..." if len(trail['summary']) > 100 else trail['summary']
            print(f"   Summary: {summary}")
        print()
    
    if len(trails) > limit:
        print(f"... and {len(trails) - limit} more trails.")
    
    return 0


def details_command(args):
    """Handle the details command."""
    print(f"\n{'='*80}")
    print(f"Getting trail details for: {args.slug}")
    print(f"{'='*80}\n")
    
    trail = get_trail_by_slug(args.slug)
    
    if not trail or not trail.get('title'):
        print("❌ Trail not found. Please check the trail slug.")
        return 1
    
    print(f"✅ Trail: {trail['title']}\n")
    print(f"URL: {trail['url']}")
    
    if trail.get('length'):
        print(f"Length: {trail['length']}")
    if trail.get('elevation_gain'):
        print(f"Elevation Gain: {trail['elevation_gain']}")
    if trail.get('route_type'):
        print(f"Route Type: {trail['route_type']}")
    if trail.get('difficulty'):
        print(f"Difficulty: {trail['difficulty']}")
    if trail.get('rating'):
        print(f"Rating: {trail['rating']}")
    
    if trail.get('summary'):
        print(f"\nDescription:\n{trail['summary']}")
    
    print()
    return 0


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="AllTrails MCP - Search and explore hiking trails",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for trails in a park
  alltrails-search search us/tennessee/great-smoky-mountains-national-park
  
  # Limit results to top 5
  alltrails-search search us/california/yosemite-national-park --limit 5
  
  # Show URLs and summaries
  alltrails-search search us/utah/zion-national-park --show-urls --show-summary
  
  # Get details about a specific trail
  alltrails-search details us/tennessee/alum-cave-trail-to-mount-leconte
"""
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser(
        'search',
        help='Search for trails in a park'
    )
    search_parser.add_argument(
        'park',
        help="Park slug (e.g., 'us/tennessee/great-smoky-mountains-national-park')"
    )
    search_parser.add_argument(
        '-l', '--limit',
        type=int,
        help='Limit the number of results displayed'
    )
    search_parser.add_argument(
        '--show-urls',
        action='store_true',
        help='Display trail URLs'
    )
    search_parser.add_argument(
        '--show-summary',
        action='store_true',
        help='Display trail summaries'
    )
    search_parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Bypass cache and fetch fresh data'
    )
    search_parser.add_argument(
        '--force-refresh',
        action='store_true',
        help='Force refresh cached data (fetch new and update cache)'
    )
    
    # Details command
    details_parser = subparsers.add_parser(
        'details',
        help='Get detailed information about a specific trail'
    )
    details_parser.add_argument(
        'slug',
        help="Trail slug (e.g., 'us/tennessee/alum-cave-trail-to-mount-leconte')"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    # Execute command
    if args.command == 'search':
        return search_command(args)
    elif args.command == 'details':
        return details_command(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
