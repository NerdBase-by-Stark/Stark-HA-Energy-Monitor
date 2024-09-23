# __init__.py
import os
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, PLATFORMS
from .coordinator import StarkEnergyMonitorCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Stark Energy Monitor from a config entry."""
    # ... existing code ...

    # Register custom panel
    panel_file_path = hass.config.path("www/stark_energy_monitor/stark_energy_monitor.html")
    panel_url = "/local/stark_energy_monitor/stark_energy_monitor.html"

    if os.path.exists(panel_file_path):
        hass.http.register_static_path(panel_url, panel_file_path)
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

    # ... existing code ...
