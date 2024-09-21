"""Sensor platform for Stark Energy Monitor."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ENERGY_KILO_WATT_HOUR, DEVICE_CLASS_ENERGY, DEVICE_CLASS_MONETARY
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        TotalEnergySensor(coordinator),
        EnergyCostSensor(coordinator),
    ]
    # Add per-device sensors
    for device_id in coordinator.devices:
        entities.append(DeviceEnergySensor(coordinator, device_id))
    # Add solar and battery sensors
    if coordinator.solar_sensors:
        entities.append(SolarEnergySensor(coordinator))
    if coordinator.battery_sensors:
        entities.append(BatterySensor(coordinator))
    async_add_entities(entities, True)

class TotalEnergySensor(SensorEntity):
    """Sensor for total energy consumption."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Total Energy Consumption"
        self._attr_unit_of_measurement = ENERGY_KILO_WATT_HOUR
        self._attr_state = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._attr_state

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()
        self._attr_state = self.coordinator.data.get("total_energy")

class EnergyCostSensor(SensorEntity):
    """Sensor for total energy cost."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Total Energy Cost"
        self._attr_unit_of_measurement = self.hass.config.currency
        self._attr_device_class = DEVICE_CLASS_MONETARY
        self._attr_state = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._attr_state

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()
        self._attr_state = self.coordinator.data.get("cost")

class DeviceEnergySensor(SensorEntity):
    """Sensor for individual device energy consumption."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.device_id = device_id
        self._attr_name = f"Energy Consumption {device_id}"
        self._attr_unit_of_measurement = ENERGY_KILO_WATT_HOUR
        self._attr_state = None

    @property
    def state(self):
        """Return the state of the sensor."""
        state = self.hass.states.get(self.device_id)
        try:
            return float(state.state)
        except (ValueError, TypeError):
            return None

class SolarEnergySensor(SensorEntity):
    """Sensor for solar energy production."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Total Solar Production"
        self._attr_unit_of_measurement = ENERGY_KILO_WATT_HOUR
        self._attr_state = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._attr_state

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()
        self._attr_state = self.coordinator.data.get("solar_energy")

class BatterySensor(SensorEntity):
    """Sensor for battery status."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Battery Level"
        self._attr_unit_of_measurement = "%"
        self._attr_state = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._attr_state

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()
        self._attr_state = self.coordinator.data.get("battery_level")
