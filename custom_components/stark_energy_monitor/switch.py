from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up switches for Stark Energy Monitor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    switches = [DeviceControlSwitch(coordinator)]
    async_add_entities(switches, True)

class DeviceControlSwitch(SwitchEntity):
    """Switch for controlling energy-critical devices."""

    def __init__(self, coordinator):
        """Initialize the switch."""
        self.coordinator = coordinator
        self._attr_name = "Critical Device Control"
        self._attr_is_on = False

    @property
    def is_on(self):
        """Return the current state of the switch."""
        return self.coordinator.get("device_control", False)

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        self.coordinator.set_device_control(True)
        await self.async_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self.coordinator.set_device_control(False)
        await self.async_update_ha_state()
