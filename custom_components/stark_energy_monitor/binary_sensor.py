import logging
from homeassistant.components.binary_sensor import BinarySensorEntity  # Updated import
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up Stark Energy Monitor binary sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    binary_sensors = [
        StarkEnergyMonitorBinarySensor(
            coordinator, "Critical Device Alert", "mdi:alert-circle"
        ),
        # Add more binary sensors as needed
    ]
    async_add_entities(binary_sensors, update_before_add=True)

class StarkEnergyMonitorBinarySensor(BinarySensorEntity):
    """Representation of a Stark Energy Monitor binary sensor."""

    def __init__(self, coordinator, name: str, icon: str):
        """Initialize the binary sensor."""
        self.coordinator = coordinator
        self._attr_name = name
        self._attr_icon = icon
        self._attr_is_on = False

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self.coordinator.data.get(self._attr_name, False)

    async def async_update(self):
        """Fetch new state data for the binary sensor."""
        await self.coordinator.async_request_refresh()
