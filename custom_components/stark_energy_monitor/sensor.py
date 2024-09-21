from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import ENERGY_KILO_WATT_HOUR, CURRENCY_DOLLAR
from .const import DOMAIN

class TotalEnergySensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Total Energy Consumption"
        self._attr_unique_id = "stark_energy_monitor_total_energy"
        self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def native_value(self):
        return self.coordinator.data.get("total_energy", 0)

class EnergyCostSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Total Energy Cost"
        self._attr_unique_id = "stark_energy_monitor_total_cost"
        self._attr_native_unit_of_measurement = CURRENCY_DOLLAR
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def native_value(self):
        return self.coordinator.data.get("total_cost", 0)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        TotalEnergySensor(coordinator),
        EnergyCostSensor(coordinator),
    ])
