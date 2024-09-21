"""Config flow for Stark Energy Monitor integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_TARIFFS,
    CONF_DEVICES,
    CONF_NOTIFICATION_PREFERENCES,
    CONF_SOLAR_INTEGRATION,
    CONF_SOLAR_SENSORS,
    CONF_BATTERY_INTEGRATION,
    CONF_BATTERY_SENSORS,
    CONF_CRITICAL_DEVICES,
)

class StarkEnergyMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Stark Energy Monitor."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._errors = {}
        self._data = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        return await self.async_step_tariffs()

    async def async_step_tariffs(self, user_input=None):
        """Configure tariff rates and times."""
        if user_input is not None:
            self._data[CONF_TARIFFS] = user_input[CONF_TARIFFS]
            return await self.async_step_devices()

        tariff_schema = vol.Schema({
            vol.Required(CONF_TARIFFS): vol.All(
                cv.ensure_list,
                [
                    vol.Schema({
                        vol.Required("tariff_name"): str,
                        vol.Required("rate"): vol.Coerce(float),
                        vol.Required("start_time"): str,
                        vol.Required("end_time"): str,
                        vol.Optional("days", default=["mon", "tue", "wed", "thu", "fri", "sat", "sun"]): [str],
                    })
                ]
            )
        })

        return self.async_show_form(
            step_id="tariffs",
            data_schema=tariff_schema,
            errors=self._errors,
        )

    async def async_step_devices(self, user_input=None):
        """Select devices to monitor."""
        if user_input is not None:
            self._data[CONF_DEVICES] = user_input[CONF_DEVICES]
            return await self.async_step_notifications()

        devices = [
            selector.EntitySelectorConfig(domain="sensor")
        ]

        device_schema = vol.Schema({
            vol.Required(CONF_DEVICES): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                    device_class="energy",
                    multiple=True
                )
            )
        })

        return self.async_show_form(
            step_id="devices",
            data_schema=device_schema,
            errors=self._errors,
        )

    async def async_step_notifications(self, user_input=None):
        """Configure notification preferences."""
        if user_input is not None:
            self._data[CONF_NOTIFICATION_PREFERENCES] = user_input
            return await self.async_step_solar()

        notification_schema = vol.Schema({
            vol.Optional("threshold", default=0): vol.Coerce(float),
            vol.Optional("notification_methods", default=["persistent_notification"]): [str],
            vol.Optional("quiet_hours", default=""): str,
        })

        return self.async_show_form(
            step_id="notifications",
            data_schema=notification_schema,
            errors=self._errors,
        )

    async def async_step_solar(self, user_input=None):
        """Configure solar integration."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_battery()

        solar_schema = vol.Schema({
            vol.Required(CONF_SOLAR_INTEGRATION, default=False): bool,
            vol.Optional(CONF_SOLAR_SENSORS): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                    device_class="power",
                    multiple=True
                )
            ),
        })

        return self.async_show_form(
            step_id="solar",
            data_schema=solar_schema,
            errors=self._errors,
        )

    async def async_step_battery(self, user_input=None):
        """Configure battery integration."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_critical_devices()

        battery_schema = vol.Schema({
            vol.Required(CONF_BATTERY_INTEGRATION, default=False): bool,
            vol.Optional(CONF_BATTERY_SENSORS): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                    device_class="battery",
                    multiple=True
                )
            ),
        })

        return self.async_show_form(
            step_id="battery",
            data_schema=battery_schema,
            errors=self._errors,
        )

    async def async_step_critical_devices(self, user_input=None):
        """Configure critical devices."""
        if user_input is not None:
            self._data[CONF_CRITICAL_DEVICES] = user_input[CONF_CRITICAL_DEVICES]
            return await self.async_step_finalize()

        critical_device_schema = vol.Schema({
            vol.Optional(CONF_CRITICAL_DEVICES): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                    multiple=True
                )
            )
        })

        return self.async_show_form(
            step_id="critical_devices",
            data_schema=critical_device_schema,
            errors=self._errors,
        )

    async def async_step_finalize(self, user_input=None):
        """Finalize configuration."""
        return self.async_create_entry(title="Stark Energy Monitor", data=self._data)
