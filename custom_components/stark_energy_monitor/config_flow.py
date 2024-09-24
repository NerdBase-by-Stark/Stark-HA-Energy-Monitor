import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_ENTITY_ID
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers import config_validation as cv
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
                # Validate input here if needed
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
                vol.Optional(CONF_TARIFFS): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=["manual", "sensor"],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        custom_value=True,
                    )
                ),
                vol.Optional(CONF_CRITICAL_DEVICES, default=[]): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        multiple=True,
                        device_class="sensor",
                        domain="sensor",
                    )
                ),
            }),
            errors= {}
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

    async def async_import_config_flow(self):
        """Handle importing config flow."""
        # Moved the potentially blocking import operation to a separate thread
        result = await self.hass.async_add_executor_job(
            importlib.import_module, f"{self.pkg_path}.{platform_name}"
        )
        return result