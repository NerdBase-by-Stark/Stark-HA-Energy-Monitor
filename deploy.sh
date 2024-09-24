#!/bin/bash

# Variables
REPO_URL="https://github.com/NerdBase-by-Stark/Stark-HA-Energy-Monitor.git"
HA_CONFIG_DIR="${1:-/config}"
CUSTOM_COMPONENTS_DIR="$HA_CONFIG_DIR/custom_components"
WWW_DIR="$HA_CONFIG_DIR/www/stark_energy_monitor"

# Clone the repository
if git clone "$REPO_URL" temp_stark_energy_monitor; then
    echo "Repository cloned successfully."
else
    echo "Error: Failed to clone repository."
    exit 1
fi

# Copy the custom component files to Home Assistant
if cp -r temp_stark_energy_monitor/custom_components/stark_energy_monitor "$CUSTOM_COMPONENTS_DIR/"; then
    echo "Custom component files copied successfully."
else
    echo "Error: Failed to copy custom component files."
    rm -rf temp_stark_energy_monitor
    exit 1
fi

# Ensure www directory exists and copy resources
if [ ! -d "$WWW_DIR" ]; then
    mkdir -p "$WWW_DIR"
fi

# Copy the HTML and other web resources to the www folder
if cp -r temp_stark_energy_monitor/www/stark_energy_monitor/* "$WWW_DIR/"; then
    echo "Web resources copied successfully."
else
    echo "Error: Failed to copy web resources."
    rm -rf temp_stark_energy_monitor
    exit 1
fi

# Clean up
rm -rf temp_stark_energy_monitor

echo "Deployment complete. Please restart Home Assistant to activate the Stark Energy Monitor integration."
