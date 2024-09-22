"""Notifications for Stark Energy Monitor."""
import logging
from homeassistant.components.notify import BaseNotificationService
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def async_get_service(hass: HomeAssistant, config: dict, discovery_info=None):
    """Set up the notification service."""
    return StarkEnergyMonitorNotificationService()

class StarkEnergyMonitorNotificationService(BaseNotificationService):
    """Notification service for Stark Energy Monitor."""

    async def async_send_message(self, message="", **kwargs):
        """Send a notification message asynchronously."""
        _LOGGER.info(f"Sending notification: {message}")
        # Implement actual notification logic here
