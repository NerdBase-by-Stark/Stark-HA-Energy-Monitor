"""Initialize the Stark Energy Monitor integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Stark Energy Monitor component."""
    hass.data.setdefault(DOMAIN, {})
    hass.http.register_static_path(
        "/stark_energy_monitor_panel.js",
        hass.config.path("custom_components/stark_energy_monitor/www/stark_energy_monitor_panel.js"),
        cache_headers=False
    )
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Stark Energy Monitor from a config entry."""
    # [Same as before]
    # Register custom panel
    hass.components.frontend.async_register_built_in_panel(
        component_name="stark_energy_monitor",
        sidebar_title="Stark Energy Monitor",
        sidebar_icon="mdi:flash",
        frontend_url_path="stark-energy-monitor",
        config={"name": "Stark Energy Monitor"},
        require_admin=False
    )
    return True
