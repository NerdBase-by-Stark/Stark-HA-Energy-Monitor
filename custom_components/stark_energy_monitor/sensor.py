# sensor.py
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity

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

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"stark_energy_monitor_{self._attr_name.lower().replace(' ', '_')}"
