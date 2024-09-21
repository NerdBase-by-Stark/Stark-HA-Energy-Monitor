"""Notifications for Stark Energy Monitor."""
from homeassistant.components.notify import BaseNotificationService
import logging

_LOGGER = logging.getLogger(__name__)

async def async_get_service(hass, config, discovery_info=None):
    """Set up the notification service."""
    return StarkEnergyMonitorNotificationService()

class StarkEnergyMonitorNotificationService(BaseNotificationService):
    """Notification service for Stark Energy Monitor."""

    def send_message(self, message="", **kwargs):
        """Send a notification message."""
        _LOGGER.info(f"Sending notification: {message}")
