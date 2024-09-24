# import logging
# from homeassistant.components.notify import BaseNotificationService
# from homeassistant.config_entries import ConfigEntry
# from homeassistant.core import HomeAssistant

# _LOGGER = logging.getLogger(__name__)

# async def async_get_service(hass, config, discovery_info=None):
#    """Set up the Stark Energy Monitor notification service."""
#    return StarkEnergyMonitorNotificationService()
#
#class StarkEnergyMonitorNotificationService(BaseNotificationService):
#    """Implementation of a notification service for Stark Energy Monitor."""
#
#@property
#def targets(self):
#    """Return a dictionary of available notification targets."""
#    return {"all_devices": "All Devices"}
#
#    async def async_send_message(self, message="", **kwargs):
#        """Send a notification message."""
#        _LOGGER.info(f"Sending notification: {message} with kwargs: {kwargs}")
#
#        # Handle optional kwargs like title and target
#        title = kwargs.get("title", "Stark Energy Monitor Notification")
#        target = kwargs.get("target", "all_devices")
#
#        _LOGGER.info(f"Notification title: {title}, target: {target}")
#        
#        # Example: Implement your actual notification sending logic here.
#        # For now, we'll just log that the notification was sent.
#        _LOGGER.info(f"Notification sent: {message}")