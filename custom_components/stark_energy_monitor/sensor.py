from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Stark Energy Monitor sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    sensors = [StarkEnergyMonitorSensor(coordinator, "Total Consumption", "kWh", "mdi:flash")]
    async_add_entities(sensors)

class StarkEnergyMonitorSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Stark Energy Monitor sensor."""

    def __init__(self, coordinator, name: str, unit: str, icon: str):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._attr_name)
