import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_ENTITY_ID
from homeassistant.core import callback
from homeassistant.helpers.selector import EntitySelector  # For selecting existing sensors
from .const import DOMAIN, CONF_SAMPLE_INTERVAL, CONF_ENABLE_NOTIFICATIONS, CONF_DATA_RETENTION_DAYS, CONF_TARIFFS, CONF_CRITICAL_DEVICES, CONF_SOLAR_INTEGRATION, CONF_BATTERY_INTEGRATION

_LOGGER = logging.getLogger(__name__)

@config_entries.HANDLERS.register(DOMAIN)
class StarkEnergyMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Stark Energy Monitor."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                # If the user has selected a tariff input method
                if user_input.get("tariff_input_method") == "manual":
                    return await self.async_step_manual_tariff(user_input)
                elif user_input.get("tariff_input_method") == "sensor":
                    return await self.async_step_select_sensor(user_input)
            except Exception as e:
                _LOGGER.error(f"Error in config flow: {e}")
                errors["base"] = "unknown_error"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default="Stark Energy Monitor"): str,
                vol.Optional("tariff_input_method", default="manual"): vol.In(["manual", "sensor"]),
            }),
            errors=errors
        )

    async def async_step_manual_tariff(self, user_input=None):
        """Handle manual tariff input."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="manual_tariff",
            data_schema=vol.Schema({
                vol.Required("tariff_name", default="Peak"): str,
                vol.Required("tariff_rate", default=0.20): vol.Coerce(float),
                vol.Required("start_time", default="17:00"): str,
                vol.Required("end_time", default="21:00"): str,
                # Additional fields for off-peak, shoulder, etc.
            }),
            errors=errors
        )

    async def async_step_select_sensor(self, user_input=None):
        """Handle sensor selection for tariffs."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="select_sensor",
            data_schema=vol.Schema({
                vol.Required(CONF_ENTITY_ID): EntitySelector({"domain": "sensor"}),  # Sensor selection
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Define the options flow."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(step_id="init")
