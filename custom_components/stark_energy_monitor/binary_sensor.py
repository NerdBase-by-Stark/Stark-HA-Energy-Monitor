"""Binary sensor platform for Stark Energy Monitor."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up the binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [PeakTimeBinarySensor(coordinator)]
    # Add critical device sensors
    for device_id in coordinator.critical_devices:
        entities.append(CriticalDeviceSensor(coordinator, device_id))
    async_add_entities(entities, True)

class PeakTimeBinarySensor(BinarySensorEntity):
    """Binary sensor indicating if it's peak time."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Is Peak Time"
        self._attr_is_on = False

    @property
    def is_on(self):
        """Return true if it is peak time."""
        current_tariff = self.coordinator.data.get("current_tariff", {})
        return current_tariff.get('tariff_name') == 'Peak'

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()

class CriticalDeviceSensor(BinarySensorEntity):
    """Binary sensor for critical device status."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.device_id = device_id
        self._attr_name = f"Critical Device {device_id} Status"
        self._attr_is_on = True

    @property
    def is_on(self):
        """Return true if the device is functioning normally."""
        status = self.coordinator.data.get("critical_devices_status", {})
        return status.get(self.device_id) != "unavailable"

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()
