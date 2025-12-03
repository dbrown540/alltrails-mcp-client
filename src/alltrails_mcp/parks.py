"""
Park slug constants and mappings for AllTrails.

This module provides easy access to all 63 US National Park slugs
for use with the AllTrails scraper.
"""

from enum import Enum
from typing import Dict


class NationalPark(Enum):
    """Enum of all 63 US National Park slugs."""
    
    # All 63 National Parks (alphabetical order)
    ACADIA = "us/maine/acadia-national-park"
    ARCHES = "us/utah/arches-national-park"
    BADLANDS = "us/south-dakota/badlands-national-park"
    BIG_BEND = "us/texas/big-bend-national-park"
    BISCAYNE = "us/florida/biscayne-national-park"
    BLACK_CANYON_OF_THE_GUNNISON = "us/colorado/black-canyon-of-the-gunnison-national-park"
    BRYCE_CANYON = "us/utah/bryce-canyon-national-park"
    CANYONLANDS = "us/utah/canyonlands-national-park"
    CAPITOL_REEF = "us/utah/capitol-reef-national-park"
    CARLSBAD_CAVERNS = "us/new-mexico/carlsbad-caverns-national-park"
    CHANNEL_ISLANDS = "us/california/channel-islands-national-park"
    CONGAREE = "us/south-carolina/congaree-national-park"
    CRATER_LAKE = "us/oregon/crater-lake-national-park"
    CUYAHOGA_VALLEY = "us/ohio/cuyahoga-valley-national-park"
    DEATH_VALLEY = "us/california/death-valley-national-park"
    DENALI = "us/alaska/denali-national-park"
    DRY_TORTUGAS = "us/florida/dry-tortugas-national-park"
    EVERGLADES = "us/florida/everglades-national-park"
    GATES_OF_THE_ARCTIC = "us/alaska/gates-of-the-arctic-national-park-and-preserve"
    GATEWAY_ARCH = "us/missouri/gateway-arch-national-park"
    GLACIER = "us/montana/glacier-national-park"
    GLACIER_BAY = "us/alaska/glacier-bay-national-park-and-preserve"
    GRAND_CANYON = "us/arizona/grand-canyon-national-park"
    GRAND_TETON = "us/wyoming/grand-teton-national-park"
    GREAT_BASIN = "us/nevada/great-basin-national-park"
    GREAT_SAND_DUNES = "us/colorado/great-sand-dunes-national-park-and-preserve"
    GREAT_SMOKY_MOUNTAINS = "us/tennessee/great-smoky-mountains-national-park"
    GUADALUPE_MOUNTAINS = "us/texas/guadalupe-mountains-national-park"
    HALEAKALA = "us/hawaii/haleakala-national-park"
    HAWAII_VOLCANOES = "us/hawaii/hawaii-volcanoes-national-park"
    HOT_SPRINGS = "us/arkansas/hot-springs-national-park"
    INDIANA_DUNES = "us/indiana/indiana-dunes-national-park"
    ISLE_ROYALE = "us/michigan/isle-royale-national-park"
    JOSHUA_TREE = "us/california/joshua-tree-national-park"
    KATMAI = "us/alaska/katmai-national-park-preserve"
    KENAI_FJORDS = "us/alaska/kenai-fjords-national-park"
    KINGS_CANYON = "us/california/kings-canyon-national-park"
    KOBUK_VALLEY = "us/alaska/kobuk-valley-national-park"
    LAKE_CLARK = "us/alaska/lake-clark-national-park-and-preserve"
    LASSEN_VOLCANIC = "us/california/lassen-volcanic-national-park"
    MAMMOTH_CAVE = "us/kentucky/mammoth-cave-national-park"
    MESA_VERDE = "us/colorado/mesa-verde-national-park"
    MOUNT_RAINIER = "us/washington/mount-rainier-national-park"
    NATIONAL_PARK_OF_AMERICAN_SAMOA = "american-samoa/national-park-of-american-samoa"
    NEW_RIVER_GORGE = "us/west-virginia/new-river-gorge-national-park-and-preserve"
    NORTH_CASCADES = "us/washington/north-cascades-national-park"
    OLYMPIC = "us/washington/olympic-national-park"
    PETRIFIED_FOREST = "us/arizona/petrified-forest-national-park"
    PINNACLES = "us/california/pinnacles-national-park"
    REDWOOD = "us/california/redwood-national-and-state-parks"
    ROCKY_MOUNTAIN = "us/colorado/rocky-mountain-national-park"
    SAGUARO = "us/arizona/saguaro-national-park"
    SEQUOIA = "us/california/sequoia-national-park"
    SHENANDOAH = "us/virginia/shenandoah-national-park"
    THEODORE_ROOSEVELT = "us/north-dakota/theodore-roosevelt-national-park"
    VIRGIN_ISLANDS = "us-virgin-islands/virgin-islands-national-park"
    VOYAGEURS = "us/minnesota/voyageurs-national-park"
    WHITE_SANDS = "us/new-mexico/white-sands-national-park"
    WIND_CAVE = "us/south-dakota/wind-cave-national-park"
    WRANGELL_ST_ELIAS = "us/alaska/wrangell-st-elias-national-park-preserve"
    YELLOWSTONE = "us/wyoming/yellowstone-national-park"
    YOSEMITE = "us/california/yosemite-national-park"
    ZION = "us/utah/zion-national-park"


# Dictionary mapping for easy lookup by name
PARK_SLUGS: Dict[str, str] = {
    # Common names (lowercase) and variations
    "acadia": NationalPark.ACADIA.value,
    "arches": NationalPark.ARCHES.value,
    "badlands": NationalPark.BADLANDS.value,
    "big bend": NationalPark.BIG_BEND.value,
    "biscayne": NationalPark.BISCAYNE.value,
    "black canyon": NationalPark.BLACK_CANYON_OF_THE_GUNNISON.value,
    "black canyon of the gunnison": NationalPark.BLACK_CANYON_OF_THE_GUNNISON.value,
    "bryce": NationalPark.BRYCE_CANYON.value,
    "bryce canyon": NationalPark.BRYCE_CANYON.value,
    "canyonlands": NationalPark.CANYONLANDS.value,
    "capitol reef": NationalPark.CAPITOL_REEF.value,
    "carlsbad": NationalPark.CARLSBAD_CAVERNS.value,
    "carlsbad caverns": NationalPark.CARLSBAD_CAVERNS.value,
    "channel islands": NationalPark.CHANNEL_ISLANDS.value,
    "congaree": NationalPark.CONGAREE.value,
    "crater lake": NationalPark.CRATER_LAKE.value,
    "cuyahoga": NationalPark.CUYAHOGA_VALLEY.value,
    "cuyahoga valley": NationalPark.CUYAHOGA_VALLEY.value,
    "death valley": NationalPark.DEATH_VALLEY.value,
    "denali": NationalPark.DENALI.value,
    "dry tortugas": NationalPark.DRY_TORTUGAS.value,
    "everglades": NationalPark.EVERGLADES.value,
    "gates of the arctic": NationalPark.GATES_OF_THE_ARCTIC.value,
    "gateway arch": NationalPark.GATEWAY_ARCH.value,
    "glacier": NationalPark.GLACIER.value,
    "glacier bay": NationalPark.GLACIER_BAY.value,
    "grand canyon": NationalPark.GRAND_CANYON.value,
    "grand teton": NationalPark.GRAND_TETON.value,
    "great basin": NationalPark.GREAT_BASIN.value,
    "great sand dunes": NationalPark.GREAT_SAND_DUNES.value,
    "great smoky mountains": NationalPark.GREAT_SMOKY_MOUNTAINS.value,
    "smoky mountains": NationalPark.GREAT_SMOKY_MOUNTAINS.value,
    "smokies": NationalPark.GREAT_SMOKY_MOUNTAINS.value,
    "guadalupe mountains": NationalPark.GUADALUPE_MOUNTAINS.value,
    "guadalupe": NationalPark.GUADALUPE_MOUNTAINS.value,
    "haleakala": NationalPark.HALEAKALA.value,
    "hawaii volcanoes": NationalPark.HAWAII_VOLCANOES.value,
    "hot springs": NationalPark.HOT_SPRINGS.value,
    "indiana dunes": NationalPark.INDIANA_DUNES.value,
    "isle royale": NationalPark.ISLE_ROYALE.value,
    "joshua tree": NationalPark.JOSHUA_TREE.value,
    "katmai": NationalPark.KATMAI.value,
    "kenai fjords": NationalPark.KENAI_FJORDS.value,
    "kenai": NationalPark.KENAI_FJORDS.value,
    "kings canyon": NationalPark.KINGS_CANYON.value,
    "kobuk valley": NationalPark.KOBUK_VALLEY.value,
    "lake clark": NationalPark.LAKE_CLARK.value,
    "lassen": NationalPark.LASSEN_VOLCANIC.value,
    "lassen volcanic": NationalPark.LASSEN_VOLCANIC.value,
    "mammoth cave": NationalPark.MAMMOTH_CAVE.value,
    "mesa verde": NationalPark.MESA_VERDE.value,
    "mount rainier": NationalPark.MOUNT_RAINIER.value,
    "rainier": NationalPark.MOUNT_RAINIER.value,
    "american samoa": NationalPark.NATIONAL_PARK_OF_AMERICAN_SAMOA.value,
    "new river gorge": NationalPark.NEW_RIVER_GORGE.value,
    "north cascades": NationalPark.NORTH_CASCADES.value,
    "olympic": NationalPark.OLYMPIC.value,
    "petrified forest": NationalPark.PETRIFIED_FOREST.value,
    "pinnacles": NationalPark.PINNACLES.value,
    "redwood": NationalPark.REDWOOD.value,
    "rocky mountain": NationalPark.ROCKY_MOUNTAIN.value,
    "saguaro": NationalPark.SAGUARO.value,
    "sequoia": NationalPark.SEQUOIA.value,
    "shenandoah": NationalPark.SHENANDOAH.value,
    "theodore roosevelt": NationalPark.THEODORE_ROOSEVELT.value,
    "virgin islands": NationalPark.VIRGIN_ISLANDS.value,
    "voyageurs": NationalPark.VOYAGEURS.value,
    "white sands": NationalPark.WHITE_SANDS.value,
    "wind cave": NationalPark.WIND_CAVE.value,
    "wrangell": NationalPark.WRANGELL_ST_ELIAS.value,
    "wrangell st elias": NationalPark.WRANGELL_ST_ELIAS.value,
    "wrangell-st. elias": NationalPark.WRANGELL_ST_ELIAS.value,
    "yellowstone": NationalPark.YELLOWSTONE.value,
    "yosemite": NationalPark.YOSEMITE.value,
    "zion": NationalPark.ZION.value,
}


def get_park_slug(name: str) -> str:
    """
    Get a park slug by common name.
    
    Args:
        name: Common park name (case-insensitive)
        
    Returns:
        Park slug for use with search_trails_in_park()
        
    Raises:
        ValueError: If park name is not found
        
    Example:
        >>> get_park_slug("Yosemite")
        'us/california/yosemite-national-park'
        >>> get_park_slug("smoky mountains")
        'us/tennessee/great-smoky-mountains-national-park'
    """
    name_lower = name.lower().strip()
    
    if name_lower in PARK_SLUGS:
        return PARK_SLUGS[name_lower]
    
    # Try to find by enum name
    try:
        enum_name = name_lower.replace(" ", "_").replace("-", "_").upper()
        return NationalPark[enum_name].value
    except KeyError:
        pass
    
    raise ValueError(
        f"Park '{name}' not found. Use NationalPark enum or provide a valid slug. "
        f"Example slugs: {list(PARK_SLUGS.keys())[:5]}"
    )


def list_parks() -> Dict[str, str]:
    """
    Get a dictionary of all available parks.
    
    Returns:
        Dictionary mapping park enum names to slugs
        
    Example:
        >>> parks = list_parks()
        >>> print(parks['YOSEMITE'])
        'us/california/yosemite-national-park'
    """
    return {park.name: park.value for park in NationalPark}
