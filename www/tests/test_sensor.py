# tests/test_sensor.py
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.stark_energy_monitor.sensor import StarkEnergyMonitorSensor

@pytest.fixture
def hass():
    return HomeAssistant()

async def test_total_consumption_sensor(hass: HomeAssistant):
    """Test the total consumption sensor."""
    assert await async_setup_component(hass, "stark_energy_monitor", {})
    await hass.async_block_till_done()
    
    state = hass.states.get("sensor.total_consumption")
    assert state is not None
    assert state.state == "0"
    assert state.attributes["unit_of_measurement"] == "kWh"
