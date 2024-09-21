"""Config flow for Stark Energy Monitor integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class StarkEnergyMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Stark Energy Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the config flow."""
        errors = {}

        if user_input is not None:
            # You can add validation logic here
            return self.async_create_entry(
                title=user_input.get("monitor_name", "Stark Energy Monitor"),
                data=user_input
            )

        # Define the form schema
        data_schema = vol.Schema({
            vol.Required("monitor_name", default="Stark Energy Monitor"): str,
            vol.Required("sample_interval", default=60): vol.All(vol.Coerce(int), vol.Range(min=1)),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Handle options flow."""
        return StarkEnergyMonitorOptionsFlow(config_entry)

class StarkEnergyMonitorOptionsFlow(config_entries.OptionsFlow):
    """Handle an options flow for Stark Energy Monitor."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options for the integration."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Options schema for managing the options
        options_schema = vol.Schema({
            vol.Optional("enable_notifications", default=True): bool,
            vol.Optional("data_retention_days", default=30): vol.Coerce(int),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema
        )
