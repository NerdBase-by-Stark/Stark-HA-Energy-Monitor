# Stark Energy Monitor Integration for Home Assistant

## Overview

Stark Energy Monitor is a comprehensive Home Assistant integration that allows you to monitor your energy consumption, costs, solar production, battery storage, and receive notifications when thresholds are exceeded. All configurations are handled through the Home Assistant UI, and the dashboard is automatically set up during installation.

## Features

- **Real-Time Energy Tracking**
- **Advanced Cost Calculations**
- **Per-Device Monitoring**
- **Solar and Battery Integration**
- **Critical Device Alerts**
- **Automatic Dashboard Setup**
- **Notifications**
- **Data Retention Management**
- **Voice Assistant Integration**

## Installation

### Via HACS (Recommended)

1. **Add Custom Repository to HACS**:

   - Open HACS in Home Assistant.
   - Go to **Integrations**.
   - Click the three dots and select **Custom repositories**.
   - Add:

     - **Repository**: `https://github.com/NerdBase-by-Stark/Stark-HA-Energy-Monitor`
     - **Category**: Integration

2. **Install the Integration**:

   - Find **Stark Energy Monitor** in HACS and install it.

3. **Restart Home Assistant**.

### Configuration

1. **Add the Integration**:

   - Go to **Configuration** > **Integrations**.
   - Click **Add Integration** and select **Stark Energy Monitor**.

2. **Follow the Setup Wizard**:

   - Configure tariffs, devices, notifications, and other settings via the UI.

## Usage

- **Access the Dashboard**:

  - Click on **Stark Energy Monitor** in the Home Assistant sidebar.

- **View Energy Data**:

  - The dashboard displays real-time and historical energy data, costs, solar production, battery status, and more.

## Updating

- **Via HACS**:

  - Updates are managed through HACS.

## Troubleshooting

- **No Manual Configurations Required**:

  - All settings are handled via the UI.

- **Check Logs**:

  - If issues arise, check the Home Assistant logs for errors related to the integration.

## License

This project is licensed under the MIT License.

## Support

For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/NerdBase-by-Stark/Stark-HA-Energy-Monitor/issues).
