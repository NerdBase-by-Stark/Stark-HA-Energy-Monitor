"""Config flow for Stark Energy Monitor integration."""
import logging
from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class StarkEnergyMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Stark Energy Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Perform validation if necessary
            return self.async_create_entry(title="Stark Energy Monitor", data=user_input)

        data_schema = vol.Schema({
            vol.Required("api_key"): str,
            # Add other configuration options as needed
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
