"""Nominatim API client."""

import asyncio
import logging
from typing import Any

import httpx

from n7m.models import GeocodingResult, ReverseGeocodingResult
from n7m.settings import settings

logger = logging.getLogger(__name__)


class NominatimClient:
    """Client for interacting with the Nominatim API."""

    def __init__(self) -> None:
        """Initialize the Nominatim client."""
        self.base_url = settings.nominatim_base_url
        self.timeout = settings.request_timeout
        self.user_agent = settings.user_agent
        self.rate_limit_delay = 1.0 / settings.max_requests_per_second
        self._last_request_time = 0.0
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent},
            )
        return self._client

    async def _rate_limit(self) -> None:
        """Enforce rate limiting."""
        current_time = asyncio.get_event_loop().time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - time_since_last_request)
        self._last_request_time = asyncio.get_event_loop().time()

    async def search(
        self,
        query: str,
        limit: int = 10,
        country_codes: str | None = None,
        addressdetails: bool = True,
        extratags: bool = False,
    ) -> list[GeocodingResult]:
        """
        Search for locations by query string.

        Args:
            query: Free-form query string
            limit: Maximum number of results (1-50)
            country_codes: Comma-separated list of country codes (e.g., "us,ca")
            addressdetails: Include address breakdown
            extratags: Include additional OSM tags

        Returns:
            List of geocoding results
        """
        await self._rate_limit()

        params: dict[str, Any] = {
            "q": query,
            "format": "json",
            "limit": min(max(1, limit), 50),
            "addressdetails": int(addressdetails),
            "extratags": int(extratags),
        }

        if country_codes:
            params["countrycodes"] = country_codes

        client = await self._get_client()
        logger.info("Searching for: %s", query)

        response = await client.get(f"{self.base_url}/search", params=params)
        response.raise_for_status()

        data = response.json()
        return [GeocodingResult.model_validate(result) for result in data]

    async def reverse(
        self,
        lat: float,
        lon: float,
        zoom: int = 18,
        addressdetails: bool = True,
        extratags: bool = False,
    ) -> ReverseGeocodingResult:
        """
        Reverse geocode coordinates to an address.

        Args:
            lat: Latitude (-90 to 90)
            lon: Longitude (-180 to 180)
            zoom: Level of detail (0-18, where 18 is building level)
            addressdetails: Include address breakdown
            extratags: Include additional OSM tags

        Returns:
            Reverse geocoding result
        """
        await self._rate_limit()

        params: dict[str, Any] = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "zoom": min(max(0, zoom), 18),
            "addressdetails": int(addressdetails),
            "extratags": int(extratags),
        }

        client = await self._get_client()
        logger.info("Reverse geocoding: %s, %s", lat, lon)

        response = await client.get(f"{self.base_url}/reverse", params=params)
        response.raise_for_status()

        data = response.json()
        return ReverseGeocodingResult.model_validate(data)

    async def lookup(
        self,
        osm_ids: str,
        addressdetails: bool = True,
        extratags: bool = False,
    ) -> list[GeocodingResult]:
        """
        Look up location details by OSM ID.

        Args:
            osm_ids: Comma-separated list of OSM IDs (e.g., "R146656,W104393803")
                    Format: [N|W|R]<id> where N=node, W=way, R=relation
            addressdetails: Include address breakdown
            extratags: Include additional OSM tags

        Returns:
            List of geocoding results
        """
        await self._rate_limit()

        params: dict[str, Any] = {
            "osm_ids": osm_ids,
            "format": "json",
            "addressdetails": int(addressdetails),
            "extratags": int(extratags),
        }

        client = await self._get_client()
        logger.info("Looking up OSM IDs: %s", osm_ids)

        response = await client.get(f"{self.base_url}/lookup", params=params)
        response.raise_for_status()

        data = response.json()
        return [GeocodingResult.model_validate(result) for result in data]

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
