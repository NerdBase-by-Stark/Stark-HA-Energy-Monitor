# tests/test_config_flow.py
import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from custom_components.stark_energy_monitor import config_flow

@pytest.mark.asyncio
async def test_config_flow(hass: HomeAssistant):
    """Test the config flow."""
    result = await hass.config_entries.flow.async_init(
        "stark_energy_monitor", context={"source": "user"}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"name": "Stark Energy Monitor"}
    )
    await hass.async_block_till_done()
    assert result["type"] == "create_entry"
    assert result["title"] == "Stark Energy Monitor"
    assert result["data"] == {"name": "Stark Energy Monitor"}
