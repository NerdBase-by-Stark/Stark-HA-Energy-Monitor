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
from homeassistant.components.frontend import DOMAIN as FRONTEND_DOMAIN
from homeassistant.helpers import aiohttp_client

from .const import (
    DOMAIN, 
    PLATFORMS, 
    CONF_SAMPLE_INTERVAL, 
    CONF_ENABLE_NOTIFICATIONS, 
    CONF_DATA_RETENTION_DAYS, 
    MIN_HA_VERSION  # Make sure this is correctly referenced from const.py
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
    from homeassistant.const import __version__ as HA_VERSION
    
    # Ensure that Home Assistant version meets the minimum required
    if AwesomeVersion(HA_VERSION) < AwesomeVersion(MIN_HA_VERSION):
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

        # Define relative URL and local path to the HTML file
        panel_url = "/local/stark_energy_monitor/stark_energy_monitor.html"
        panel_file_path = hass.config.path("www/stark_energy_monitor/stark_energy_monitor.html")

        if os.path.exists(panel_file_path):
            # Register the static path for the custom panel
            hass.http.register_static_path(panel_url, panel_file_path, cache_headers=False)
            
            # Register the panel in the Home Assistant frontend
            hass.components.frontend.async_register_built_in_panel(
                "iframe",
                "Stark Energy Monitor",
                "mdi:flash",
                config={"url": panel_url},
                require_admin=False
            )
            _LOGGER.info("Stark Energy Monitor panel registered successfully.")
        else:
            _LOGGER.warning(f"Panel HTML file not found at {panel_file_path}")

        # Continue with other setup steps
        await handle_lovelace_dashboard(hass)
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        _LOGGER.info("Stark Energy Monitor setup complete.")
        return True
    except Exception as e:
        _LOGGER.error(f"Error setting up Stark Energy Monitor: {e}")
        raise ConfigEntryNotReady


async def handle_lovelace_dashboard(hass: HomeAssistant):
    """Handle Lovelace dashboard integration for Stark Energy Monitor."""
    try:
        # Correct way to get the Lovelace mode
        lovelace_mode = hass.data.get("lovelace", {}).get("mode", "storage")
        if lovelace_mode != "storage":
            dashboard_file_path = hass.config.path("custom_components/stark_energy_monitor/dashboard/stark_energy_monitor_dashboard.yaml")
            if os.path.exists(dashboard_file_path):
                try:
                    with open(dashboard_file_path, 'r') as dashboard_file:
                        dashboard_config = yaml.safe_load(dashboard_file)
                        # Here you can add code to integrate the YAML dashboard if needed
                        _LOGGER.info("Loaded Stark Energy Monitor dashboard in YAML mode.")
                except Exception as e:
                    _LOGGER.error(f"Failed to load YAML dashboard: {e}")
            else:
                _LOGGER.warning(f"Dashboard YAML file not found at {dashboard_file_path}")
        else:
            _LOGGER.info("Lovelace is in storage mode; please add resources via UI.")
    except Exception as e:
        _LOGGER.error(f"Error handling Lovelace dashboard: {e}")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info("Stark Energy Monitor unloaded")
    return unload_ok
