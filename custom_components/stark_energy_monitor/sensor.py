# sensor.py
import logging
from homeassistant.helpers.entity import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry: ConfigEntry, async_add_entities):
    """Set up Stark Energy Monitor sensors."""
    sensors = [
        StarkEnergyMonitorSensor(
            hass, config_entry, "Total Consumption", UnitOfEnergy.KILO_WATT_HOUR, "mdi:flash"
        ),
        StarkEnergyMonitorSensor(
            hass, config_entry, "Real-Time Consumption", UnitOfPower.WATT, "mdi:flash-circle"
        ),
        # Add more sensors as needed
    ]
    async_add_entities(sensors, update_before_add=True)

class StarkEnergyMonitorSensor(SensorEntity):
    """Representation of a Stark Energy Monitor sensor."""

    def __init__(self, hass, config_entry: ConfigEntry, name: str, unit: str, icon: str):
        """Initialize the sensor."""
        self.hass = hass
        self._config = config_entry.data
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_native_value = None

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            _LOGGER.debug(f"Fetching data for sensor: {self._attr_name}")
            # Implement your data fetching logic here
            # Example:
            # self._attr_native_value = await fetch_energy_data(self._config)
            self._attr_native_value = 0  # Placeholder value for testing
            _LOGGER.debug(f"Updated {self._attr_name} to state: {self._attr_native_value}")
        except Exception as e:
            _LOGGER.error(f"Error updating sensor {self._attr_name}: {e}")
            self._attr_native_value = None
