from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ENERGY_KILO_WATT_HOUR
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors for Stark Energy Monitor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        TotalEnergySensor(coordinator),
        EnergyCostSensor(coordinator),
    ]
    async_add_entities(sensors, True)

class StarkEnergyMonitorBaseSensor(SensorEntity):
    """Base sensor for Stark Energy Monitor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_device_class = "energy"
        self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()

class TotalEnergySensor(StarkEnergyMonitorBaseSensor):
    """Total energy consumption sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Total Energy Consumption"
        self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR

    @property
    def native_value(self):
        """Return the current value."""
        return self.coordinator.get("total_energy", 0)

class EnergyCostSensor(StarkEnergyMonitorBaseSensor):
    """Total energy cost sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Total Energy Cost"
        self._attr_native_unit_of_measurement = self.coordinator.get("currency", "USD")

    @property
    def native_value(self):
        """Return the current value."""
        return self.coordinator.get("total_cost", 0)
