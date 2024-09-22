"""Initialize the Stark Energy Monitor integration."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME

from .sensor import StarkEnergyMonitorSensor
from .binary_sensor import StarkEnergyMonitorBinarySensor

_LOGGER = logging.getLogger(__name__)

DOMAIN = "stark_energy_monitor"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Stark Energy Monitor component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Stark Energy Monitor from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # Initialize sensors and binary sensors
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")
    )

    # Frontend panel registration is handled via manifest.json
    # No need to manually register the frontend panel here

    _LOGGER.info("Stark Energy Monitor setup complete")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    unload_ok &= await hass.config_entries.async_forward_entry_unload(entry, "binary_sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    _LOGGER.info("Stark Energy Monitor unloaded")
    return unload_ok
