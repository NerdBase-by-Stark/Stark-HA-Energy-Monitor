import logging
from homeassistant.components.sensor import SensorEntity  # Updated import
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import UnitOfEnergy, UnitOfPower

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up Stark Energy Monitor sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    sensors = [
        StarkEnergyMonitorSensor(
            coordinator, "Total Consumption", UnitOfEnergy.KILO_WATT_HOUR, "mdi:flash"
        ),
        StarkEnergyMonitorSensor(
            coordinator, "Real-Time Consumption", UnitOfPower.WATT, "mdi:flash-circle"
        ),
        # Add more sensors as needed
    ]
    async_add_entities(sensors, update_before_add=True)

class StarkEnergyMonitorSensor(SensorEntity):
    """Representation of a Stark Energy Monitor sensor."""

    def __init__(self, coordinator, name: str, unit: str, icon: str):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_native_value = None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._attr_name, None)

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self.coordinator.async_request_refresh()
