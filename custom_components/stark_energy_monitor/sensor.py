import logging
from homeassistant.helpers.entity import Entity
from homeassistant.const import ENERGY_KILO_WATT_HOUR, POWER_WATT

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class StarkEnergyMonitorSensor(Entity):
    """Representation of a Stark Energy Monitor sensor."""

    def __init__(self, hass, config_entry, name, unit, icon):
        """Initialize the sensor."""
        self._hass = hass
        self._config = config_entry.data
        self._name = name
        self._unit = unit
        self._icon = icon
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon."""
        return self._icon

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            _LOGGER.debug(f"Fetching data for sensor: {self._name}")
            # Implement your data fetching logic here
            # Example:
            # self._state = await fetch_energy_data(self._config)
            self._state = 0  # Placeholder value for testing
            _LOGGER.debug(f"Updated {self._name} to state: {self._state}")
        except Exception as e:
            _LOGGER.error(f"Error updating sensor {self._name}: {e}")
            self._state = None

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Stark Energy Monitor sensors."""
    sensors = [
        StarkEnergyMonitorSensor(
            hass, config_entry, "Total Consumption", ENERGY_KILO_WATT_HOUR, "mdi:flash"
        ),
        StarkEnergyMonitorSensor(
            hass, config_entry, "Real-Time Consumption", POWER_WATT, "mdi:flash-circle"
        ),
        # Add more sensors as needed
    ]
    async_add_entities(sensors, update_before_add=True)
