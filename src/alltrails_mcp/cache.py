"""
Trail data caching module using SQLite.

Caches trail search results to minimize requests to AllTrails and avoid rate limiting.
Cache expires after 7 days.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Default cache location - in current working directory
DEFAULT_CACHE_DB = Path.cwd() / "trails_cache.db"


class TrailCache:
    """Manages cached trail data in SQLite database."""
    
    def __init__(self, db_path: Optional[Path] = None, cache_days: int = 7):
        """
        Initialize the trail cache.
        
        Args:
            db_path: Path to SQLite database file. Defaults to ~/.alltrails_mcp/trails_cache.db
            cache_days: Number of days before cache expires (default: 7)
        """
        self.db_path = db_path or DEFAULT_CACHE_DB
        self.cache_days = cache_days
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist."""
        # Create directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create parks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parks (
                    park_slug TEXT PRIMARY KEY,
                    last_updated TIMESTAMP NOT NULL,
                    trail_count INTEGER NOT NULL
                )
            """)
            
            # Create trails table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    park_slug TEXT NOT NULL,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    summary TEXT,
                    difficulty TEXT,
                    length TEXT,
                    rating TEXT,
                    trail_data JSON,
                    FOREIGN KEY (park_slug) REFERENCES parks(park_slug) ON DELETE CASCADE
                )
            """)
            
            # Create index for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_park_slug 
                ON trails(park_slug)
            """)
            
            conn.commit()
            logger.info(f"Cache database initialized at {self.db_path}")
    
    def get_cached_trails(self, park_slug: str) -> Optional[List[Dict]]:
        """
        Get cached trails for a park if cache is still valid.
        
        Args:
            park_slug: Park identifier
            
        Returns:
            List of trail dictionaries if cache is valid, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if park exists and cache is valid
            cursor.execute("""
                SELECT last_updated, trail_count 
                FROM parks 
                WHERE park_slug = ?
            """, (park_slug,))
            
            result = cursor.fetchone()
            if not result:
                logger.info(f"No cache found for park: {park_slug}")
                return None
            
            last_updated_str, trail_count = result
            last_updated = datetime.fromisoformat(last_updated_str)
            cache_age = datetime.now() - last_updated
            
            # Check if cache is expired
            if cache_age > timedelta(days=self.cache_days):
                logger.info(f"Cache expired for {park_slug} (age: {cache_age.days} days)")
                return None
            
            # Get cached trails
            cursor.execute("""
                SELECT name, url, summary, difficulty, length, rating, trail_data
                FROM trails
                WHERE park_slug = ?
                ORDER BY id
            """, (park_slug,))
            
            trails = []
            for row in cursor.fetchall():
                name, url, summary, difficulty, length, rating, trail_data_json = row
                
                # Use trail_data if available, otherwise construct from individual fields
                if trail_data_json:
                    trail = json.loads(trail_data_json)
                else:
                    trail = {
                        "name": name,
                        "url": url,
                        "summary": summary or "",
                        "difficulty": difficulty or "",
                        "length": length or "",
                        "rating": rating or ""
                    }
                trails.append(trail)
            
            logger.info(f"Cache hit for {park_slug}: {len(trails)} trails (age: {cache_age.days} days)")
            return trails
    
    def save_trails(self, park_slug: str, trails: List[Dict], limit: int = 15):
        """
        Save trails to cache, replacing any existing cache for this park.
        
        Args:
            park_slug: Park identifier
            trails: List of trail dictionaries
            limit: Maximum number of trails to cache (default: 15)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Delete existing cached data for this park
            cursor.execute("DELETE FROM trails WHERE park_slug = ?", (park_slug,))
            cursor.execute("DELETE FROM parks WHERE park_slug = ?", (park_slug,))
            
            # Limit trails to save
            trails_to_save = trails[:limit]
            
            # Insert park record
            cursor.execute("""
                INSERT INTO parks (park_slug, last_updated, trail_count)
                VALUES (?, ?, ?)
            """, (park_slug, datetime.now().isoformat(), len(trails_to_save)))
            
            # Insert trail records
            for trail in trails_to_save:
                cursor.execute("""
                    INSERT INTO trails (
                        park_slug, name, url, summary, difficulty, length, rating, trail_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    park_slug,
                    trail.get("name", ""),
                    trail.get("url", ""),
                    trail.get("summary", ""),
                    trail.get("difficulty", ""),
                    trail.get("length", ""),
                    trail.get("rating", ""),
                    json.dumps(trail)  # Store complete trail data as JSON
                ))
            
            conn.commit()
            logger.info(f"Cached {len(trails_to_save)} trails for {park_slug}")
    
    def clear_cache(self, park_slug: Optional[str] = None):
        """
        Clear cached data.
        
        Args:
            park_slug: If provided, only clear cache for this park. 
                      If None, clear entire cache.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if park_slug:
                cursor.execute("DELETE FROM trails WHERE park_slug = ?", (park_slug,))
                cursor.execute("DELETE FROM parks WHERE park_slug = ?", (park_slug,))
                logger.info(f"Cleared cache for {park_slug}")
            else:
                cursor.execute("DELETE FROM trails")
                cursor.execute("DELETE FROM parks")
                logger.info("Cleared entire cache")
            
            conn.commit()
    
    def get_cache_info(self) -> Dict:
        """
        Get information about the cache.
        
        Returns:
            Dictionary with cache statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get total parks cached
            cursor.execute("SELECT COUNT(*) FROM parks")
            total_parks = cursor.fetchone()[0]
            
            # Get total trails cached
            cursor.execute("SELECT COUNT(*) FROM trails")
            total_trails = cursor.fetchone()[0]
            
            # Get parks with cache info
            cursor.execute("""
                SELECT park_slug, last_updated, trail_count 
                FROM parks 
                ORDER BY last_updated DESC
            """)
            
            parks = []
            for park_slug, last_updated_str, trail_count in cursor.fetchall():
                last_updated = datetime.fromisoformat(last_updated_str)
                cache_age = datetime.now() - last_updated
                is_expired = cache_age > timedelta(days=self.cache_days)
                
                parks.append({
                    "park_slug": park_slug,
                    "last_updated": last_updated_str,
                    "cache_age_days": cache_age.days,
                    "trail_count": trail_count,
                    "is_expired": is_expired
                })
            
            return {
                "db_path": str(self.db_path),
                "cache_days": self.cache_days,
                "total_parks": total_parks,
                "total_trails": total_trails,
                "parks": parks
            }


def search_trails_with_cache(
    park_slug: str, 
    cache: Optional[TrailCache] = None,
    force_refresh: bool = False,
    limit: int = 15
) -> List[Dict]:
    """
    Search for trails with caching support.
    
    Args:
        park_slug: Park identifier
        cache: TrailCache instance (creates default if None)
        force_refresh: If True, bypass cache and fetch fresh data
        limit: Maximum number of trails to cache
        
    Returns:
        List of trail dictionaries
    """
    from alltrails_mcp.scraper import search_trails_in_park
    
    if cache is None:
        cache = TrailCache()
    
    # Try to get from cache first (unless force refresh)
    if not force_refresh:
        cached_trails = cache.get_cached_trails(park_slug)
        if cached_trails is not None:
            return cached_trails
    
    # Cache miss or force refresh - fetch from AllTrails
    logger.info(f"Fetching fresh data for {park_slug}")
    trails = search_trails_in_park(park_slug)
    
    # Save to cache if we got results
    if trails:
        cache.save_trails(park_slug, trails, limit=limit)
    
    return trails
