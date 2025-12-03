# AllTrails MCP Server
# Copyright (c) 2025 Srinath Srinivasan
# Licensed under the MIT License - see LICENSE file for details

import asyncio
import sys
from datetime import datetime

print(f"{datetime.now()}: Starting AllTrails MCP server", file=sys.stderr)

try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
    
    print("MCP imports successful", file=sys.stderr)
    
    # Import AllTrails scraper and cache
    try:
        from app.alltrails_scraper import get_trail_by_slug
    except ImportError:
        from alltrails_mcp.scraper import get_trail_by_slug
    
    from alltrails_mcp.cache import TrailCache, search_trails_with_cache
    from alltrails_mcp.parks import get_park_slug, list_parks
    print("AllTrails scraper and cache imports successful", file=sys.stderr)
    
    # Initialize cache
    cache = TrailCache()
    
    server = Server("alltrails-mcp")
    
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        print("list_tools called", file=sys.stderr)
        return [
            types.Tool(
                name="search_trails",
                description="Search for trails in a specific national park using AllTrails data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "park": {
                            "type": "string",
                            "description": "Park name (e.g., 'Yosemite', 'Grand Canyon') or slug in format 'us/state/park-name' (e.g., 'us/tennessee/great-smoky-mountains-national-park')"
                        }
                    },
                    "required": ["park"]
                }
            ),
            types.Tool(
                name="get_trail_details",
                description="Get detailed information about a specific trail by its AllTrails slug",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slug": {
                            "type": "string",
                            "description": "Trail slug from AllTrails URL (the part after '/trail/')"
                        }
                    },
                    "required": ["slug"]
                }
            ),
            types.Tool(
                name="list_parks",
                description="List all available US National Parks with their names and slugs. Use this to discover valid park names before searching for trails.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        print(f"call_tool: {name} with {arguments}", file=sys.stderr)
        
        try:
            if name == "search_trails":
                park = arguments.get("park")
                if not park:
                    return [types.TextContent(type="text", text="Park parameter is required")]
                
                # Try to resolve park name to slug (supports both names and slugs)
                try:
                    park_slug = get_park_slug(park)
                    print(f"Searching trails for park: {park} -> {park_slug} (using cache)", file=sys.stderr)
                except ValueError:
                    # If not a known park name, assume it's a slug and try it directly
                    park_slug = park
                    print(f"Searching trails for park: {park} (as slug, using cache)", file=sys.stderr)
                
                # Check if cached before fetching
                cached_trails = cache.get_cached_trails(park_slug)
                if cached_trails:
                    print(f"✓ Cache HIT - returning {len(cached_trails)} cached trails", file=sys.stderr)
                    trails = cached_trails
                else:
                    print(f"✗ Cache MISS - fetching from AllTrails", file=sys.stderr)
                    trails = search_trails_with_cache(park_slug, cache=cache, limit=15)
                
                if not trails:
                    return [types.TextContent(
                        type="text",
                        text=f"No trails found for park: {park}. Please check the park name or slug format."
                    )]
                
                response = f"Found {len(trails)} trails in {park}:\n\n"
                for i, trail in enumerate(trails, 1):
                    response += f"{i}. **{trail['name']}**\n"
                    if trail.get('difficulty'):
                        response += f"   - Difficulty: {trail['difficulty']}\n"
                    if trail.get('length'):
                        response += f"   - Length: {trail['length']}\n"
                    if trail.get('rating'):
                        response += f"   - Rating: {trail['rating']}\n"
                    if trail.get('summary'):
                        summary = trail['summary'][:80] + "..." if len(trail['summary']) > 80 else trail['summary']
                        response += f"   - Summary: {summary}\n"
                    response += f"   - URL: {trail['url']}\n\n"
                
                return [types.TextContent(type="text", text=response)]
            
            elif name == "list_parks":
                print("Listing all available parks", file=sys.stderr)
                parks = list_parks()
                
                response = "# Available US National Parks\n\n"
                response += f"Total: {len(parks)} parks\n\n"
                
                for park_name, slug in sorted(parks.items()):
                    # Format enum name to title case
                    display_name = park_name.replace('_', ' ').title()
                    response += f"- **{display_name}**\n"
                    response += f"  - Slug: `{slug}`\n"
                
                return [types.TextContent(type="text", text=response)]
            
            elif name == "get_trail_details":
                slug = arguments.get("slug")
                if not slug:
                    return [types.TextContent(type="text", text="Slug parameter is required")]
                
                print(f"Getting trail details for: {slug}", file=sys.stderr)
                trail = get_trail_by_slug(slug)
                
                if not trail or not trail.get('title'):
                    return [types.TextContent(
                        type="text",
                        text=f"Trail not found for slug: {slug}. Please check the trail slug."
                    )]
                
                # Format detailed trail information
                response = f"# {trail['title']}\n\n"
                if trail.get('length'):
                    response += f"**Length:** {trail['length']}\n"
                if trail.get('elevation_gain'):
                    response += f"**Elevation Gain:** {trail['elevation_gain']}\n"
                if trail.get('route_type'):
                    response += f"**Route Type:** {trail['route_type']}\n"
                if trail.get('difficulty'):
                    response += f"**Difficulty:** {trail['difficulty']}\n"
                if trail.get('rating'):
                    response += f"**Rating:** {trail['rating']}\n"
                response += f"**URL:** {trail['url']}\n\n"
                
                if trail.get('summary'):
                    response += f"**Description:**\n{trail['summary']}\n"
                
                return [types.TextContent(type="text", text=response)]
            
            else:
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
        
        except Exception as e:
            print(f"Error in tool {name}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def main():
        print("Creating server capabilities", file=sys.stderr)
        
        capabilities = types.ServerCapabilities(
            tools=types.ToolsCapability(listChanged=False)
        )
        
        init_options = InitializationOptions(
            server_name="alltrails",
            server_version="0.1.0",
            capabilities=capabilities
        )
        
        print("Starting stdio server", file=sys.stderr)
        
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            print("AllTrails MCP server running", file=sys.stderr)
            await server.run(
                read_stream,
                write_stream,
                initialization_options=init_options
            )
    
    if __name__ == "__main__":
        asyncio.run(main())
        
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)