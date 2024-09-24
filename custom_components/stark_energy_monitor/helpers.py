"""Helper functions for Stark Energy Monitor."""
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

# async def send_notification(hass: HomeAssistant, message, methods):
#    """Send notifications using specified methods."""
#    for method in methods:
#        if method == "persistent_notification":
#            await hass.services.async_call(
#                'persistent_notification',
#                'create',
#                {
#                    'title': 'Stark Energy Monitor Alert',
#                    'message': message,
#                }
#            )
#        elif method == "mobile_app":
#            await hass.services.async_call(
#                'notify',
#                'mobile_app',
#                {
#                    'message': message,
#                }
#            )
#        # Add other notification methods as needed
