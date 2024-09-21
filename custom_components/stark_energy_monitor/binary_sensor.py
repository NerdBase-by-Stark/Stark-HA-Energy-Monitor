from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors for Stark Energy Monitor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [CriticalDeviceSensor(coordinator)]
    async_add_entities(sensors, True)

class CriticalDeviceSensor(BinarySensorEntity):
    """Binary sensor for monitoring critical devices."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Critical Device Status"
        self._attr_is_on = False

    @property
    def is_on(self):
        """Return true if the device is operating normally."""
        return self.coordinator.get("critical_device_status", False)

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()
