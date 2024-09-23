"""Initialize the Stark Energy Monitor integration."""
import logging
import os
import yaml
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from awesomeversion.awesomeversion import AwesomeVersion
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, CONF_NAME
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.discovery import async_load_platform
from .const import (
    DOMAIN, 
    PLATFORMS, 
    CONF_SAMPLE_INTERVAL, 
    CONF_ENABLE_NOTIFICATIONS, 
    CONF_DATA_RETENTION_DAYS, 
    MIN_HA_VERSION
)
from .coordinator import StarkEnergyMonitorCoordinator

_LOGGER = logging.getLogger(__name__)

# Default update interval and basic configuration schema
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_NAME, default="Stark Energy Monitor"): str,
        vol.Optional(CONF_SAMPLE_INTERVAL, default=60): vol.All(vol.Coerce(int), vol.Range(min=1, max=300)),
        vol.Optional(CONF_ENABLE_NOTIFICATIONS, default=False): bool,
        vol.Optional(CONF_DATA_RETENTION_DAYS, default=30): vol.All(vol.Coerce(int), vol.Range(min=1)),
    }),
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Stark Energy Monitor component."""
    if AwesomeVersion(hass.config.version) < AwesomeVersion(MIN_HA_VERSION):
        _LOGGER.error(f"Home Assistant version {MIN_HA_VERSION} or higher required.")
        return False

    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Stark Energy Monitor from a config entry."""
    try:
        coordinator = StarkEnergyMonitorCoordinator(hass)
        await coordinator.async_config_entry_first_refresh()

        hass.data[DOMAIN][entry.entry_id] = {
            "coordinator": coordinator,
        }

        # Handle Lovelace in storage mode or YAML mode
        await handle_lovelace_dashboard(hass)

        # Register platforms (e.g., sensor)
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        _LOGGER.info("Stark Energy Monitor setup complete.")
        return True
    except Exception as e:
        _LOGGER.error(f"Error setting up Stark Energy Monitor: {e}")
        raise ConfigEntryNotReady

async def handle_lovelace_dashboard(hass: HomeAssistant):
    """Handle Lovelace dashboard integration for Stark Energy Monitor."""
    if "lovelace" in hass.data and hass.data["lovelace"]["mode"] != "storage":
        dashboard_file_path = hass.config.path("custom_components/stark_energy_monitor/dashboard/stark_energy_monitor_dashboard.yaml")
        if os.path.exists(dashboard_file_path):
            with open(dashboard_file_path, 'r') as dashboard_file:
                dashboard_config = yaml.safe_load(dashboard_file)
                # Handle YAML mode setup (if applicable)
                _LOGGER.info("Loaded Stark Energy Monitor dashboard in YAML mode.")
        else:
            _LOGGER.warning(f"Dashboard YAML file not found at {dashboard_file_path}")
    else:
        _LOGGER.info("Lovelace is in storage mode; please add resources via UI.")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info("Stark Energy Monitor unloaded")
    return unload_ok
