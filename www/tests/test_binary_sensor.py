# tests/test_binary_sensor.py
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.stark_energy_monitor.binary_sensor import StarkEnergyMonitorBinarySensor

@pytest.fixture
def hass():
    return HomeAssistant()

async def test_critical_device_binary_sensor(hass: HomeAssistant):
    """Test the critical device binary sensor."""
    assert await async_setup_component(hass, "stark_energy_monitor", {})
    await hass.async_block_till_done()
    
    state = hass.states.get("binary_sensor.critical_device_alert")
    assert state is not None
    assert state.state == "off"