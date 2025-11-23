# N7M - Nominatim MCP Server

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## AI-Powered Geocoding via Model Context Protocol

N7M provides OpenStreetMap's Nominatim geocoding service through the Model Context Protocol (MCP), enabling AI assistants to convert addresses to coordinates, search for locations, and perform reverse geocoding.

## Features

- **Location Search** - Find coordinates for any address or location name
- **Reverse Geocoding** - Convert coordinates to detailed addresses
- **OSM Lookup** - Get details for specific OpenStreetMap objects
- **Rate Limiting** - Automatic compliance with Nominatim's 1 req/sec policy
- **Global Coverage** - Powered by OpenStreetMap's worldwide data
- **Async Design** - Built with modern async Python

## Getting Started

The fastest way to use N7M is with `uvx` (no installation required):

### For Claude Desktop

Add this to your MCP Settings file:

```json
{
  "mcpServers": {
    "n7m": {
      "command": "uvx",
      "args": ["n7m-mcp"]
    }
  }
}
```

### Quick Test

Once configured, ask your AI assistant:

```text
"Find the coordinates for the Eiffel Tower"
"What's the address at coordinates 40.7128, -74.0060?"
"Search for coffee shops near Times Square, NYC"
```

## Usage Examples

### Search for a Location

```python
# Ask your AI: "Find the White House"
# Returns: coordinates, address, and details
```

### Reverse Geocode

```python
# Ask your AI: "What's at 51.5074 N, 0.1278 W?"
# Returns: Detailed address for London coordinates
```

### OSM Lookup

```python
# Ask your AI: "Look up OSM relation R146656"
# Returns: Details for New York City
```

## Environment Variables

Configure N7M behavior with environment variables (all use `N7M_` prefix):

| Variable                 | Default                             | Description                 |
| ------------------------ | ----------------------------------- | --------------------------- |
| `N7M_NOMINATIM_BASE_URL` | https://nominatim.openstreetmap.org | Nominatim server URL        |
| `N7M_REQUEST_TIMEOUT`    | 30                                  | Request timeout (seconds)   |
| `N7M_USER_AGENT`         | n7m-mcp/0.1.0                       | User agent for API requests |
| `N7M_LOG_LEVEL`          | INFO                                | Logging level               |

## Docker

Run N7M in a container:

```bash
# Pull the image
docker pull ghcr.io/jonpspri/n7m-mcp:latest

# Run with stdio transport
docker run -i ghcr.io/jonpspri/n7m-mcp:latest

# Run with HTTP transport
docker run -p 8000:8000 ghcr.io/jonpspri/n7m-mcp:latest --transport http --host 0.0.0.0
```

## Development

```bash
# Clone the repository
git clone https://github.com/jonpspri/n7m-mcp.git
cd n7m-mcp

# Install dependencies
uv sync

# Run the server locally
uv run n7m-mcp

# Run tests
uv run pytest

# Run quality checks
uv run ruff check
uv run mypy src/n7m/
```

## Rate Limiting

N7M automatically enforces Nominatim's usage policy of 1 request per second. All requests are rate-limited to ensure compliance with OpenStreetMap's fair use guidelines.

## Data Attribution

All geocoding data comes from OpenStreetMap contributors. When using N7M, you're accessing data from:

Copyright OpenStreetMap contributors

Please include this attribution when displaying results to end users.

## License

Apache 2.0 - see [LICENSE](LICENSE) file.

## Support

- **Issues**: [GitHub Issues](https://github.com/jonpspri/n7m-mcp/issues)
- **Repository**: [GitHub](https://github.com/jonpspri/n7m-mcp)

## Related Projects

- [DataBeak](https://github.com/jonpspri/databeak) - MCP server for CSV data operations
- [FastMCP](https://github.com/jlowin/fastmcp) - Framework for building MCP servers
