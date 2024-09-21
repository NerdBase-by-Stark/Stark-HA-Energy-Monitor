#!/bin/bash

# Deployment script for Stark Energy Monitor integration

# Variables
REPO_URL="https://github.com/NerdBase-by-Stark/Stark-HA-Energy-Monitor.git"
HA_CONFIG_DIR="/config"
CUSTOM_COMPONENTS_DIR="$HA_CONFIG_DIR/custom_components"

# Clone the repository
git clone $REPO_URL temp_stark_energy_monitor

# Copy the custom component to Home Assistant
cp -r temp_stark_energy_monitor/custom_components/stark_energy_monitor $CUSTOM_COMPONENTS_DIR/

# Clean up
rm -rf temp_stark_energy_monitor

echo "Deployment complete. Restart Home Assistant to activate the Stark Energy Monitor integration."
