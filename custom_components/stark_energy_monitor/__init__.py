"""Initialize the Stark Energy Monitor integration."""
import logging
import os
import yaml
import importlib
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS
from .coordinator import StarkEnergyMonitorCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Stark Energy Monitor component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Stark Energy Monitor from a config entry."""
    try:
        # Use async execution to avoid blocking the event loop
        await hass.async_add_executor_job(importlib.import_module, "custom_components.stark_energy_monitor.config_flow")

        # Initialize coordinator for handling updates
        coordinator = StarkEnergyMonitorCoordinator(hass)
        await coordinator.async_config_entry_first_refresh()

        hass.data[DOMAIN][entry.entry_id] = {
            "coordinator": coordinator,
        }

        # Handle dashboard file if in YAML mode (skip for storage mode)
        if "lovelace" in hass.data and hass.data["lovelace"]["mode"] != "storage":
            dashboard_file_path = hass.config.path("custom_components/stark_energy_monitor/dashboard/stark_energy_monitor_dashboard.yaml")
            if os.path.exists(dashboard_file_path):
                with open(dashboard_file_path, 'r') as dashboard_file:
                    dashboard_config = yaml.safe_load(dashboard_file)
                    _LOGGER.info("Loaded Stark Energy Monitor dashboard in YAML mode.")
            else:
                _LOGGER.warning(f"Dashboard YAML file not found at {dashboard_file_path}")
        else:
            _LOGGER.info("Lovelace is in storage mode; please add resources via UI.")

        # Register custom panel
        panel_file_path = hass.config.path("custom_components/stark_energy_monitor/panel/stark_energy_monitor.html")
        if os.path.exists(panel_file_path):
            hass.http.register_static_path(
                "/local/stark_energy_monitor_panel.html", panel_file_path
            )
            hass.components.frontend.async_register_built_in_panel(
                "iframe",
                "Stark Energy Monitor",
                "mdi:flash",
                config={"url": "/local/stark_energy_monitor_panel.html"}
            )
            _LOGGER.info("Stark Energy Monitor panel registered successfully.")
        else:
            _LOGGER.warning(f"Panel HTML file not found at {panel_file_path}")

        # Forward setup to all platforms
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        _LOGGER.info("Stark Energy Monitor setup complete.")
        return True
    except Exception as e:
        _LOGGER.error(f"Error setting up Stark Energy Monitor: {e}")
        raise ConfigEntryNotReady

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    _LOGGER.info("Stark Energy Monitor unloaded")
    return unload_ok
