# Stark Energy Monitor Integration for Home Assistant

## Overview

Stark Energy Monitor is a comprehensive Home Assistant integration that allows you to monitor your energy consumption, costs, solar production, battery storage, and receive notifications when thresholds are exceeded.

## Features

- **Real-Time Energy Tracking**: Monitor energy usage for all devices.
- **Advanced Cost Calculations**: Supports complex tariff structures.
- **Per-Device Monitoring**: Track individual device consumption.
- **Solar and Battery Integration**: Monitor solar production and battery levels.
- **Critical Device Alerts**: Receive alerts for critical devices.
- **Customizable Dashboards**: Pre-configured dashboard with customizable cards.
- **Notifications**: Configurable alerts with various notification methods.
- **Data Retention Management**: Control how long data is stored.
- **Voice Assistant Integration**: Interact with your energy data using voice commands.

## Installation

### Via HACS (Recommended)

1. Open HACS in your Home Assistant instance.
2. Go to the "Integrations" section.
3. Click the "+" button to add a new integration.
4. Click the three dots in the top right corner and select "Custom repositories".
5. Add your repository URL:

   - **Repository**: `https://github.com/NerdBase-by-Stark/Stark-HA-Energy-Monitor`
   - **Category**: Integration

6. After adding the repository, find **Stark Energy Monitor** in the list of integrations and install it.
7. Restart Home Assistant.

### Manual Installation

1. Clone or download this repository.
2. Copy the `custom_components/stark_energy_monitor` directory to your Home Assistant's `custom_components` directory.
3. Copy the `dashboard/stark_energy_monitor_dashboard.yaml` to your Home Assistant's `lovelace` directory.
4. Restart Home Assistant.

## Configuration

### Using the UI

1. Go to **Configuration** > **Integrations** in Home Assistant.
2. Click on **Add Integration** and search for **Stark Energy Monitor**.
3. Follow the wizard to set up your tariffs, devices, and preferences.

### Configuration Options

- **Tariffs**: Define multiple tariffs with rates, times, and days.
- **Devices**: Select which devices to monitor.
- **Notifications**: Set thresholds, methods, and quiet hours.
- **Solar and Battery**: Enable integration and select sensors.
- **Critical Devices**: Tag devices for advanced monitoring.

## Usage

- Access the Stark Energy Monitor dashboard via Home Assistant UI.
- View real-time and historical energy consumption, costs, and more.
- Receive notifications based on your preferences.

## Updating

- Updates can be managed directly through HACS.
- For manual installations, repeat the installation steps with the new version.

## Troubleshooting

- Ensure all sensors are correctly configured in Home Assistant.
- Check the logs for any error messages related to the `stark_energy_monitor` integration.
- Restart Home Assistant after making changes.

## License

This project is licensed under the MIT License.

## Support

For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/NerdBase-by-Stark/Stark-HA-Energy-Monitor/issues).
