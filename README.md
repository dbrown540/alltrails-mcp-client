# AllTrails MCP Client

A Model Context Protocol (MCP) server and Python package for searching hiking trails from AllTrails.com. Includes smart caching to avoid rate limiting.

## ⚠️ Important: Rate Limiting

**AllTrails.com implements CAPTCHA and rate limiting.** This package includes a caching system to minimize requests:

- ✅ **Cache-first**: Stores up to 15 trails per park for 7 days
- 🔄 **Automatic refresh**: Updates cache after expiration
- 💾 **SQLite storage**: Local database (`trails_cache.db`)
- 🚫 **Use sparingly**: Best for personal, low-volume usage

## Features

- 🥾 Search trails by US National Park (all 63 parks supported)
- 📍 Get detailed trail information
- 💾 Smart caching system (7-day cache)
- 🤖 MCP server for Claude Desktop integration
- 🛠️ CLI tools for quick searches
- 🐍 Python API for programmatic access

## Installation

### From PyPI (when published)
```bash
pip install alltrails-mcp
```

### Development Install
```bash
git clone https://github.com/dbrown540/alltrails-mcp-client.git
cd alltrails-mcp-client
pip install -e .
```

## Quick Start

### Python API
```python
from alltrails_mcp import NationalPark, search_trails_with_cache

# Search with automatic caching
trails = search_trails_with_cache(NationalPark.YOSEMITE.value)

for trail in trails[:5]:
    print(f"{trail['name']} - {trail['difficulty']} - {trail['length']}")
```

### CLI
```bash
# Search trails
alltrails-search search us/california/yosemite-national-park --limit 5

# Get trail details
alltrails-search details us/california/half-dome-trail
```

### MCP Server (Claude Desktop)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "alltrails": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/alltrails-mcp-client/src/alltrails_mcp/server.py"]
    }
  }
}
```

Then ask Claude: "Find trails in Yosemite National Park"

## National Parks

All 63 US National Parks are available via the `NationalPark` enum:

```python
from alltrails_mcp import NationalPark, get_park_slug, list_parks

# Use enum
park = NationalPark.YOSEMITE
slug = park.value  # 'us/california/yosemite-national-park'

# Look up by name
slug = get_park_slug("Yellowstone")

# List all parks
all_parks = list_parks()
```

See `PARKS_SUMMARY.md` for complete list.

## Cache Management

```python
from alltrails_mcp import TrailCache

cache = TrailCache()

# Get cache info
info = cache.get_cache_info()
print(f"Parks cached: {info['total_parks']}")

# Clear specific park
cache.clear_cache("us/california/yosemite-national-park")

# Clear entire cache
cache.clear_cache()

# Force refresh (bypass cache)
from alltrails_mcp import search_trails_with_cache
trails = search_trails_with_cache(park_slug, force_refresh=True)
```

Cache location: `./trails_cache.db` (in current directory)

## Examples

See the `examples/` directory:
- `demo.py` - Simple demonstration of key features

Run with:
```bash
python examples/demo.py --park ZION
python examples/demo.py --stats
python examples/demo.py --clear-cache
```

## Project Structure

```
alltrails-mcp-client/
├── src/alltrails_mcp/      # Main package
│   ├── __init__.py          # Package exports
│   ├── scraper.py           # AllTrails scraping logic
│   ├── cache.py             # SQLite caching system
│   ├── parks.py             # National Park enums
│   ├── server.py            # MCP server
│   └── cli.py               # Command-line interface
├── examples/                # Example scripts
├── pyproject.toml          # Package configuration
└── README.md               # This file
```

## API Reference

### Core Functions

**`search_trails_in_park(park_slug: str) -> List[Dict]`**
- Search for trails (no caching)
- Returns: List of trail dictionaries

**`search_trails_with_cache(park_slug: str, cache=None, force_refresh=False, limit=15) -> List[Dict]`**
- Search with automatic caching
- Returns cached data if valid (<7 days old)

**`get_trail_by_slug(slug: str) -> Dict`**
- Get detailed trail information
- Example slug: `us/tennessee/alum-cave-trail`

### Trail Dictionary Format

```python
{
    "name": "Half Dome Trail",
    "url": "https://www.alltrails.com/trail/...",
    "summary": "Experience this 14.2-mile...",
    "difficulty": "Hard",
    "length": "14.2 mi",
    "rating": "4.8"
}
```

## Publishing to PyPI

See `PUBLISHING.md` for detailed instructions.

Quick steps:
```bash
# Build
python -m build

# Upload
twine upload dist/*
```

## License

MIT License - See LICENSE.md

## Acknowledgments

- Original MCP server by Srinath Srinivasan
- Forked and enhanced by Danny Brown
- Trail data from [AllTrails](https://www.alltrails.com/)
- Built with [Model Context Protocol](https://modelcontextprotocol.io/)

## Disclaimer

This tool scrapes publicly available data from AllTrails. Use responsibly and respect AllTrails' terms of service. The caching system helps minimize requests.
