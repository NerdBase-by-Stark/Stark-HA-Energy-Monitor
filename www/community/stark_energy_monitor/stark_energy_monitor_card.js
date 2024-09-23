// www/community/stark_energy_monitor/stark_energy_monitor_card.js
import { LitElement, html, css } from 'https://unpkg.com/lit-element?module';

class StarkEnergyMonitorCard extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {},
    };
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  render() {
    const entityId = this.config.entity;
    const stateObj = this.hass.states[entityId];

    if (!stateObj) {
      return html`<ha-card>Entity not found: ${entityId}</ha-card>`;
    }

    const consumption = stateObj.state;
    const unit = stateObj.attributes.unit_of_measurement || 'W';

    return html`
      <ha-card header="Stark Energy Monitor">
        <div style="padding: 16px;">
          Real-Time Consumption: ${consumption} ${unit}
        </div>
      </ha-card>
    `;
  }

  getCardSize() {
    return 1;
  }
}

customElements.define('stark-energy-monitor-card', StarkEnergyMonitorCard);
