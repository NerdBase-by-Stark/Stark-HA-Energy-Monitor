// stark_energy_monitor_card.js
import { LitElement, html, css } from 'lit';

class StarkEnergyMonitorCard extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {},
      _state: {},
    };
  }

  static get styles() {
    return css`
      ha-card {
        padding: 16px;
      }
      h1 {
        margin-top: 0;
      }
      .consumption {
        font-size: 2em;
        font-weight: bold;
      }
    `;
  }

  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  set hass(hass) {
    this._hass = hass;
    if (this.config && hass.states[this.config.entity]) {
      this._state = hass.states[this.config.entity].state;
    }
  }

  render() {
    return html`
      <ha-card>
        <h1>Stark Energy Monitor</h1>
        <div>
          Real-Time Consumption:
          <span class="consumption">${this._state || '--'} W</span>
        </div>
      </ha-card>
    `;
  }

  getCardSize() {
    return 1;
  }
}

customElements.define('stark-energy-monitor-card', StarkEnergyMonitorCard);
