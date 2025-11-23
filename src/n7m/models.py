"""Pydantic models for Nominatim API responses."""

from typing import Any

from pydantic import BaseModel, Field


class NominatimAddress(BaseModel):
    """Address components from Nominatim."""

    house_number: str | None = None
    road: str | None = None
    suburb: str | None = None
    city: str | None = None
    county: str | None = None
    state: str | None = None
    postcode: str | None = None
    country: str | None = None
    country_code: str | None = None


class GeocodingResult(BaseModel):
    """Result from geocoding search."""

    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    lat: str
    lon: str
    display_name: str
    address: NominatimAddress | None = None
    boundingbox: list[str] = Field(default_factory=list)
    importance: float | None = None
    class_: str | None = Field(None, alias="class")
    type: str | None = None
    extratags: dict[str, Any] | None = None


class ReverseGeocodingResult(BaseModel):
    """Result from reverse geocoding."""

    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    lat: str
    lon: str
    display_name: str
    address: NominatimAddress
    boundingbox: list[str] = Field(default_factory=list)
    class_: str | None = Field(None, alias="class")
    type: str | None = None
    importance: float | None = None
    extratags: dict[str, Any] | None = None
