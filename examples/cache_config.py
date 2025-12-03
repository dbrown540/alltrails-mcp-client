#!/usr/bin/env python3
"""
Example: Configuring Cache Expiration

Shows different ways to configure how long trail data is cached.
"""

import os
from pathlib import Path
from alltrails_mcp import TrailCache, search_trails_with_cache, NationalPark

print("="*80)
print("Cache Configuration Examples")
print("="*80)
print()

# Example 1: Using default cache (7 days)
print("1. Default cache (7 days):")
cache_default = TrailCache()
print(f"   Cache location: {cache_default.db_path}")
print(f"   Expiration: {cache_default.cache_days} days")
print()

# Example 2: Custom expiration (programmatic)
print("2. Custom expiration (14 days) - programmatic:")
cache_14days = TrailCache(cache_days=14)
print(f"   Expiration: {cache_14days.cache_days} days")
print()

# Example 3: Using environment variable
print("3. Using environment variable:")
os.environ['ALLTRAILS_CACHE_DAYS'] = '30'
# Note: Environment variable is read when module is imported
print(f"   Set ALLTRAILS_CACHE_DAYS=30")
print(f"   To use: export ALLTRAILS_CACHE_DAYS=30 before running your script")
print()

# Example 4: Custom location AND expiration
print("4. Custom location and expiration:")
custom_path = Path.home() / "my_trail_cache.db"
cache_custom = TrailCache(db_path=custom_path, cache_days=3)
print(f"   Cache location: {cache_custom.db_path}")
print(f"   Expiration: {cache_custom.cache_days} days")
print()

# Example 5: Using cache with search
print("5. Using configured cache with search:")
cache = TrailCache(cache_days=14)
park = NationalPark.YOSEMITE.value

# Check if cached
cached_trails = cache.get_cached_trails(park)
if cached_trails:
    print(f"   ✓ Cache HIT: {len(cached_trails)} trails cached for Yosemite")
else:
    print(f"   ✗ Cache MISS: No cached data for Yosemite")
    print(f"   (Would fetch and cache for {cache.cache_days} days)")
print()

print("="*80)
print("Configuration Priority (highest to lowest):")
print("1. Programmatic: TrailCache(cache_days=14)")
print("2. Environment: ALLTRAILS_CACHE_DAYS=14")
print("3. Default: 7 days")
print("="*80)
