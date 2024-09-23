# const.py
"""Constants for the Stark Energy Monitor integration."""

DOMAIN = "stark_energy_monitor"

PLATFORMS = ["sensor", "binary_sensor", "switch", "notify"]

CONF_MONITOR_NAME = "monitor_name"
CONF_SAMPLE_INTERVAL = "sample_interval"
CONF_ENABLE_NOTIFICATIONS = "enable_notifications"
CONF_DATA_RETENTION_DAYS = "data_retention_days"
CONF_TARIFFS = "tariffs"  # Added for tariff support
CONF_CRITICAL_DEVICES = "critical_devices"  # Added for critical device monitoring
CONF_SOLAR_INTEGRATION = "solar_integration"
CONF_BATTERY_INTEGRATION = "battery_integration"
MIN_HA_VERSION = "2023.10.0"  # Define the minimum Home Assistant version required