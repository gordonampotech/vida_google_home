"""The Vida Google Home integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN] = entry.data
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    if DOMAIN in hass.data:
        del hass.data[DOMAIN]
    return True
