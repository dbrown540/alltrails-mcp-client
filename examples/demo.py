#!/usr/bin/env python3
"""
Simple demo of alltrails-mcp package features.

Usage:
    python demo.py                              # Demo with cache (default: Yosemite)
    python demo.py --park ZION                  # Demo specific park
    python demo.py --no-cache                   # Demo without cache
    python demo.py --clear-cache                # Clear cache first
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import argparse
from alltrails_mcp import (
    NationalPark, 
    TrailCache, 
    search_trails_with_cache
)


def demo_with_cache(park: NationalPark):
    """Demo trail search with caching."""
    cache = TrailCache()
    park_slug = park.value
    
    print(f"🔍 Searching {park.name.replace('_', ' ').title()}...")
    trails = search_trails_with_cache(park_slug, cache=cache, limit=15)
    
    if trails:
        print(f"✅ Found {len(trails)} trails\n")
        for i, trail in enumerate(trails[:3], 1):
            print(f"{i}. {trail['name']}")
            if trail.get('difficulty'):
                print(f"   Difficulty: {trail['difficulty']}")
            if trail.get('length'):
                print(f"   Length: {trail['length']}")
            print()
    else:
        print("❌ No trails found (may be rate limited)\n")
    
    return trails


def demo_without_cache(park: NationalPark):
    """Demo trail search without caching."""
    from alltrails_mcp import search_trails_in_park
    
    park_slug = park.value
    print(f"🔍 Searching {park.name.replace('_', ' ').title()} (no cache)...")
    trails = search_trails_in_park(park_slug)
    
    if trails:
        print(f"✅ Found {len(trails)} trails\n")
        for i, trail in enumerate(trails[:3], 1):
            print(f"{i}. {trail['name']}")
    else:
        print("❌ No trails found (may be rate limited)\n")
    
    return trails


def show_cache_stats():
    """Show cache statistics."""
    cache = TrailCache()
    info = cache.get_cache_info()
    
    print("\n📊 Cache Statistics")
    print(f"   Location: {info['db_path']}")
    print(f"   Parks cached: {info['total_parks']}")
    print(f"   Total trails: {info['total_trails']}")


def main():
    parser = argparse.ArgumentParser(description="Demo AllTrails MCP package")
    parser.add_argument(
        "--park",
        type=str,
        default="YOSEMITE",
        help="Park name from NationalPark enum"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cache before running"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show cache statistics"
    )
    
    args = parser.parse_args()
    
    # Get park enum
    try:
        park = NationalPark[args.park.upper()]
    except KeyError:
        print(f"❌ Invalid park: {args.park}")
        print(f"\nAvailable parks: {', '.join([p.name for p in list(NationalPark)[:5]])}...")
        return 1
    
    # Clear cache if requested
    if args.clear_cache:
        cache = TrailCache()
        cache.clear_cache()
        print("🗑️  Cache cleared\n")
    
    # Run demo
    if args.no_cache:
        trails = demo_without_cache(park)
    else:
        trails = demo_with_cache(park)
    
    # Show stats if requested
    if args.stats:
        show_cache_stats()
    
    return 0 if trails else 1


if __name__ == "__main__":
    sys.exit(main())
