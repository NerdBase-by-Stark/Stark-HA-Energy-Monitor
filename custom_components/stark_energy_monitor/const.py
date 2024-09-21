"""Constants for the Stark Energy Monitor integration."""

DOMAIN = "stark_energy_monitor"

PLATFORMS = ["sensor", "binary_sensor"]

DEFAULT_NAME = "Stark Energy Monitor"

DATA_UPDATE_INTERVAL = 60  # in seconds

CONF_TARIFFS = "tariffs"
CONF_DEVICES = "devices"
CONF_NOTIFICATION_PREFERENCES = "notification_preferences"
CONF_DATA_RETENTION_DAYS = "data_retention_days"
CONF_SOLAR_INTEGRATION = "solar_integration"
CONF_SOLAR_SENSORS = "solar_sensors"
CONF_BATTERY_INTEGRATION = "battery_integration"
CONF_BATTERY_SENSORS = "battery_sensors"
CONF_CRITICAL_DEVICES = "critical_devices"
