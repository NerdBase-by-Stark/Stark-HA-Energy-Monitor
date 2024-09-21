class StarkEnergyMonitorCard extends HTMLElement {
    set hass(hass) {
        if (!this.content) {
            this.innerHTML = `
                <ha-card header="Stark Energy Monitor">
                    <div class="card-content">
                        <p>Total Energy Consumption: <span id="total-energy"></span></p>
                        <p>Total Energy Cost: <span id="total-cost"></span></p>
                    </div>
                </ha-card>
            `;
            this.content = this.querySelector('div');
        }

        const totalEnergy = hass.states['sensor.total_energy_consumption'];
        const totalCost = hass.states['sensor.total_energy_cost'];

        if (totalEnergy) {
            this.content.querySelector('#total-energy').textContent = `${totalEnergy.state} ${totalEnergy.attributes.unit_of_measurement}`;
        }
        if (totalCost) {
            this.content.querySelector('#total-cost').textContent = `${totalCost.state} ${totalCost.attributes.unit_of_measurement}`;
        }
    }

    setConfig(config) {
        if (!config.entity) {
            throw new Error('You need to define an entity');
        }
        this.config = config;
    }

    static getStubConfig() {
        return { entity: "sensor.total_energy_consumption" }
    }
}

customElements.define('stark-energy-monitor-card', StarkEnergyMonitorCard);
