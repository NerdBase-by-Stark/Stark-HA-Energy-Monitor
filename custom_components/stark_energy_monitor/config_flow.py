import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class StarkEnergyMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Stark Energy Monitor", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("sample_interval", default=30): int,
                vol.Required("enable_notifications", default=True): bool,
                vol.Required("data_retention_days", default=30): int,
            }),
            errors=errors
        )

    @staticmethod
    @config_entries.HANDLERS.register(DOMAIN)
    async def async_get_options_flow(config_entry):
        return StarkEnergyMonitorOptionsFlow(config_entry)

class StarkEnergyMonitorOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("enable_notifications", default=self.config_entry.options.get("enable_notifications", True)): bool,
                vol.Required("data_retention_days", default=self.config_entry.options.get("data_retention_days", 30)): int,
            })
        )
