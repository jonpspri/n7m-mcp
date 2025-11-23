"""Basic tests for n7m."""

import pytest

from n7m import __version__


def test_version() -> None:
    """Test that version is set."""
    assert __version__ == "0.1.0"


def test_import_server() -> None:
    """Test that server module can be imported."""
    from n7m import server  # noqa: F401


def test_import_client() -> None:
    """Test that client module can be imported."""
    from n7m import client  # noqa: F401


def test_import_models() -> None:
    """Test that models module can be imported."""
    from n7m import models  # noqa: F401


@pytest.mark.asyncio
async def test_client_creation() -> None:
    """Test that NominatimClient can be created."""
    from n7m.client import NominatimClient

    client = NominatimClient()
    assert client is not None
    assert client.base_url == "https://nominatim.openstreetmap.org"
    await client.close()
