"""Initialize the Stark Energy Monitor integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Stark Energy Monitor component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Stark Energy Monitor from a config entry."""
    _LOGGER.info(f"Setting up Stark Energy Monitor with entry: {entry.as_dict()}")
    hass.data[DOMAIN][entry.entry_id] = {
        "monitor_name": entry.data.get("monitor_name", "Stark Energy Monitor"),
        "sample_interval": entry.data.get("sample_interval", 60)
    }
    
    # Forward the setup to the platforms listed in PLATFORMS
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register custom panel
    hass.components.frontend.async_register_built_in_panel(
        component_name="custom",
        sidebar_title="Stark Energy Monitor",
        sidebar_icon="mdi:flash",
        frontend_url_path="stark-energy-monitor",
        config={
            "_panel_custom": {
                "name": "stark-energy-monitor-panel",
                "module_url": "/local/stark_energy_monitor_panel.js",
                "trust_external": False,
            }
        },
        require_admin=False,
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
