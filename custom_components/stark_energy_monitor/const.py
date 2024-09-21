"""Constants for the Stark Energy Monitor integration."""

DOMAIN = "stark_energy_monitor"

PLATFORMS = ["sensor", "binary_sensor", "switch", "notify"]

CONF_MONITOR_NAME = "monitor_name"
CONF_SAMPLE_INTERVAL = "sample_interval"
CONF_ENABLE_NOTIFICATIONS = "enable_notifications"
CONF_DATA_RETENTION_DAYS = "data_retention_days"
