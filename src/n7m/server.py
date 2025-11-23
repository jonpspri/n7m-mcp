"""Main FastMCP server for N7M."""

import logging
from argparse import ArgumentParser
from pathlib import Path

from fastmcp import FastMCP
from smithery.decorators import smithery

from n7m._version import __version__
from n7m.client import NominatimClient
from n7m.models import GeocodingResult, ReverseGeocodingResult

logger = logging.getLogger(__name__)


def _load_instructions() -> str:
    """Load instructions from the markdown file."""
    instructions_path = Path(__file__).parent / "instructions.md"
    try:
        return instructions_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.warning("Instructions file not found at %s", instructions_path)
        return "N7M MCP Server - Instructions file not available"
    except (PermissionError, OSError, UnicodeDecodeError):
        logger.exception("Error loading instructions")
        return "N7M MCP Server - Error loading instructions"


# Initialize FastMCP server
mcp = FastMCP("N7M", instructions=_load_instructions(), version=__version__)

# Global client instance
_client: NominatimClient | None = None


def get_client() -> NominatimClient:
    """Get or create the Nominatim client."""
    global _client
    if _client is None:
        _client = NominatimClient()
    return _client


@mcp.tool()
async def search(
    query: str,
    limit: int = 10,
    country_codes: str | None = None,
    addressdetails: bool = True,
    extratags: bool = False,
) -> list[GeocodingResult]:
    """
    Search for locations by query string.

    Args:
        query: Free-form query string (e.g., "1600 Pennsylvania Ave, Washington DC")
        limit: Maximum number of results to return (1-50)
        country_codes: Limit results to specific countries (comma-separated codes, e.g., "us,ca")
        addressdetails: Include detailed address breakdown
        extratags: Include additional OpenStreetMap tags

    Returns:
        List of geocoding results with coordinates and address details
    """
    client = get_client()
    return await client.search(
        query=query,
        limit=limit,
        country_codes=country_codes,
        addressdetails=addressdetails,
        extratags=extratags,
    )


@mcp.tool()
async def reverse(
    lat: float,
    lon: float,
    zoom: int = 18,
    addressdetails: bool = True,
    extratags: bool = False,
) -> ReverseGeocodingResult:
    """
    Convert coordinates to an address (reverse geocoding).

    Args:
        lat: Latitude (-90 to 90)
        lon: Longitude (-180 to 180)
        zoom: Detail level (0-18, where 18=building, 16=street, 12=town, 4=state, 0=country)
        addressdetails: Include detailed address breakdown
        extratags: Include additional OpenStreetMap tags

    Returns:
        Reverse geocoding result with address and location details
    """
    client = get_client()
    return await client.reverse(
        lat=lat,
        lon=lon,
        zoom=zoom,
        addressdetails=addressdetails,
        extratags=extratags,
    )


@mcp.tool()
async def lookup(
    osm_ids: str,
    addressdetails: bool = True,
    extratags: bool = False,
) -> list[GeocodingResult]:
    """
    Look up location details by OpenStreetMap ID.

    Args:
        osm_ids: Comma-separated OSM IDs with type prefix (e.g., "R146656,W104393803")
                Format: [N|W|R]<id> where N=node, W=way, R=relation
        addressdetails: Include detailed address breakdown
        extratags: Include additional OpenStreetMap tags

    Returns:
        List of geocoding results for the specified OSM objects
    """
    client = get_client()
    return await client.lookup(
        osm_ids=osm_ids,
        addressdetails=addressdetails,
        extratags=extratags,
    )


@smithery.server()
def create_server() -> FastMCP:
    """Create and return the Smithery FastMCP server instance."""
    return mcp


def main() -> None:
    """Start the N7M server."""
    parser = ArgumentParser(description="N7M - Nominatim MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport method",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for HTTP/SSE transport",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP/SSE transport",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level",
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info(
        "Starting N7M with %s transport",
        args.transport,
    )

    run_args: dict[str, str | int] = {"transport": args.transport}
    if args.transport != "stdio":
        run_args["host"] = args.host
        run_args["port"] = args.port

    # Run the server
    mcp.run(**run_args)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
