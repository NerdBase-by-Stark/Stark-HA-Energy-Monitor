import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_ENTITY_ID
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import (
    DOMAIN,
    CONF_SAMPLE_INTERVAL,
    CONF_ENABLE_NOTIFICATIONS,
    CONF_DATA_RETENTION_DAYS,
    CONF_TARIFFS,
    CONF_CRITICAL_DEVICES,
)

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
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            except Exception as e:
                _LOGGER.error(f"Error in config flow: {e}")
                errors["base"] = "unknown_error"

        # Define the options form with manual input or sensor selection for tariffs
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default="Stark Energy Monitor"): str,
                vol.Optional(CONF_SAMPLE_INTERVAL, default=60): vol.All(vol.Coerce(int), vol.Range(min=1, max=300)),
                vol.Optional(CONF_ENABLE_NOTIFICATIONS, default=False): bool,
                vol.Optional(CONF_DATA_RETENTION_DAYS, default=30): vol.All(vol.Coerce(int), vol.Range(min=1)),
                # Tariff mode selection: Manual or Sensor
                vol.Required(CONF_TARIFFS, default="manual"): vol.In(["manual", "sensor"]),
                vol.Optional(CONF_CRITICAL_DEVICES, default=[]): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        multiple=True,
                        domain="sensor",
                    )
                ),
            }),
            errors=errors
        )

    async def async_step_manual(self, user_input=None):
        """Step to configure manual tariffs."""
        if user_input is not None:
            return self.async_create_entry(title="Manual Tariff Configuration", data=user_input)

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema({
                vol.Required("peak_rate", default=0.20): vol.Coerce(float),
                vol.Required("offpeak_rate", default=0.10): vol.Coerce(float),
                vol.Required("peak_start", default="17:00"): str,
                vol.Required("peak_end", default="21:00"): str,
            })
        )

    async def async_step_sensor(self, user_input=None):
        """Step to configure sensor-based tariffs."""
        if user_input is not None:
            return self.async_create_entry(title="Sensor Tariff Configuration", data=user_input)

        return self.async_show_form(
            step_id="sensor",
            data_schema=vol.Schema({
                vol.Required("tariff_sensor"): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        multiple=False,
                        domain="sensor"
                    )
                ),
                vol.Required("peak_start", default="17:00"): str,
                vol.Required("peak_end", default="21:00"): str,
            })
        )

    async def async_step_user(self, user_input=None):
        """Handle initial step for manual or sensor configuration."""
        if user_input:
            # Determine if the user selected Manual or Sensor
            if user_input.get(CONF_TARIFFS) == "manual":
                return await self.async_step_manual()
            elif user_input.get(CONF_TARIFFS) == "sensor":
                return await self.async_step_sensor()

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow handler."""
        return StarkEnergyMonitorOptionsFlowHandler(config_entry)


class StarkEnergyMonitorOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Stark Energy Monitor."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(CONF_SAMPLE_INTERVAL, default=self.config_entry.options.get(CONF_SAMPLE_INTERVAL, 60)): vol.All(vol.Coerce(int), vol.Range(min=1, max=300)),
                vol.Optional(CONF_ENABLE_NOTIFICATIONS, default=self.config_entry.options.get(CONF_ENABLE_NOTIFICATIONS, False)): bool,
                vol.Optional(CONF_DATA_RETENTION_DAYS, default=self.config_entry.options.get(CONF_DATA_RETENTION_DAYS, 30)): vol.All(vol.Coerce(int), vol.Range(min=1)),
                vol.Optional(CONF_TARIFFS, default=self.config_entry.options.get(CONF_TARIFFS)): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        multiple=False,
                        domain="sensor"
                    )
                ),
                vol.Optional(CONF_CRITICAL_DEVICES, default=self.config_entry.options.get(CONF_CRITICAL_DEVICES, [])): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        multiple=True,
                        domain="sensor"
                    )
                ),
            })
        )
