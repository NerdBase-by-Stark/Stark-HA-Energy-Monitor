// stark_energy_monitor_card.js
class StarkEnergyMonitorCard extends HTMLElement {
  set hass(hass) {
    if (!this._initialized) {
      const shadow = this.attachShadow({ mode: 'open' });
      const card = document.createElement('ha-card');
      card.header = 'Stark Energy Monitor';

      const content = document.createElement('div');
      content.style.padding = '16px';

      const consumption = document.createElement('div');
      consumption.id = 'consumption';
      consumption.innerHTML = 'Real-Time Consumption: -- W';

      content.appendChild(consumption);
      card.appendChild(content);
      shadow.appendChild(card);

      this._consumptionElement = consumption;
      this._initialized = true;
    }

    const entityId = this.config.entity;
    const state = hass.states[entityId];
    if (state) {
      this._consumptionElement.innerHTML =
        `Real-Time Consumption: ${state.state} ${state.attributes.unit_of_measurement || 'W'}`;
    }
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  getCardSize() {
    return 1;
  }
}

customElements.define('stark-energy-monitor-card', StarkEnergyMonitorCard);
