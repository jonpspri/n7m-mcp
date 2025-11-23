# N7M - Nominatim Geocoding MCP Server

## Overview

N7M provides access to OpenStreetMap's Nominatim geocoding service through the
Model Context Protocol. Use these tools to convert addresses to coordinates,
coordinates to addresses, and search for locations worldwide.

## Available Tools

### search

Search for locations by query string. Returns coordinates and detailed address
information.

**Example queries:**

- "1600 Pennsylvania Avenue, Washington, DC"
- "Eiffel Tower, Paris"
- "Tokyo Station"
- "Starbucks near Central Park"

**Parameters:**

- `query`: The search query (required)
- `limit`: Maximum results to return (1-50, default: 10)
- `country_codes`: Limit to specific countries (e.g., "us,ca,mx")
- `addressdetails`: Include address breakdown (default: true)
- `extratags`: Include additional OSM tags (default: false)

### reverse

Convert coordinates (latitude/longitude) to an address.

**Example usage:**

- Latitude: 40.7128, Longitude: -74.0060 (New York City)
- Latitude: 51.5074, Longitude: -0.1278 (London)

**Parameters:**

- `lat`: Latitude (-90 to 90, required)
- `lon`: Longitude (-180 to 180, required)
- `zoom`: Detail level (0-18, default: 18)
  - 18: building level
  - 16: street level
  - 12: town level
  - 8: county level
  - 4: state level
  - 0: country level
- `addressdetails`: Include address breakdown (default: true)
- `extratags`: Include additional OSM tags (default: false)

### lookup

Look up location details by OpenStreetMap ID.

**Example OSM IDs:**

- "R146656" (New York City relation)
- "W104393803" (Eiffel Tower way)
- "N123456789" (specific node)

**Parameters:**

- `osm_ids`: Comma-separated OSM IDs with prefix (N/W/R) (required)
- `addressdetails`: Include address breakdown (default: true)
- `extratags`: Include additional OSM tags (default: false)

## Rate Limiting

Nominatim has a usage policy of 1 request per second. This server automatically
enforces rate limiting to comply with OpenStreetMap's fair use policy.

## Data Attribution

All geocoding data comes from OpenStreetMap contributors. When displaying
results, please include attribution:

"© OpenStreetMap contributors"

## Best Practices

1. **Be specific**: More detailed queries return better results
2. **Use country codes**: When possible, limit searches to specific countries
3. **Respect rate limits**: The server enforces 1 req/sec automatically
4. **Cache results**: Avoid repeated identical queries
5. **Use appropriate zoom**: For reverse geocoding, choose the right detail level

## Configuration

Environment variables (optional):

- `N7M_NOMINATIM_BASE_URL`: Custom Nominatim server (default: official OSM)
- `N7M_REQUEST_TIMEOUT`: Request timeout in seconds (default: 30)
- `N7M_USER_AGENT`: Custom user agent (default: "n7m-mcp/0.1.0")
- `N7M_LOG_LEVEL`: Logging level (default: "INFO")
