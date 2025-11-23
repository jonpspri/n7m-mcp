"""Settings for the N7M MCP server."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class N7MSettings(BaseSettings):
    """Configuration settings for N7M."""

    model_config = SettingsConfigDict(env_prefix="N7M_")

    # Nominatim API settings
    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    request_timeout: int = 30
    user_agent: str = "n7m-mcp/0.1.0"

    # Rate limiting
    max_requests_per_second: float = 1.0  # Nominatim policy: 1 request/second

    # Server settings
    log_level: str = "INFO"


settings = N7MSettings()
