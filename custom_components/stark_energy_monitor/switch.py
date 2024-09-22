import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import StarkEnergyMonitorCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up switches for Stark Energy Monitor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    switches = [DeviceControlSwitch(coordinator)]
    async_add_entities(switches)

class DeviceControlSwitch(SwitchEntity):
    """Switch for controlling energy-critical devices."""

    def __init__(self, coordinator: StarkEnergyMonitorCoordinator):
        """Initialize the switch."""
        self.coordinator = coordinator
        self._attr_name = "Critical Device Control"
        self._attr_icon = "mdi:power"

    @property
    def is_on(self):
        """Return the current state of the switch."""
        return self.coordinator.data.get("device_control", False)

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        _LOGGER.debug("Turning on Critical Device Control")
        await self.coordinator.async_set_device_control(True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.debug("Turning off Critical Device Control")
        await self.coordinator.async_set_device_control(False)
        self.async_write_ha_state()

    async def async_update(self):
        """Fetch new state data for the switch."""
        await self.coordinator.async_request_refresh()
