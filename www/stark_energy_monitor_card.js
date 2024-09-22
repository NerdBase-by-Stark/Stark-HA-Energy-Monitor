class StarkEnergyMonitorCard extends HTMLElement {
  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error("You need to define an entity");
    }
    this.innerHTML = `
      <ha-card>
        <h1>Stark Energy Monitor</h1>
        <div>Real-Time Consumption: <span id="consumption">--</span> W</div>
      </ha-card>
    `;
    this._entity = config.entity;
  }

  set hass(hass) {
    if (!this._entity) return;
    const state = hass.states[this._entity];
    if (state) {
      this.querySelector("#consumption").innerText = state.state;
    }
  }

  getCardSize() {
    return 1;
  }
}

customElements.define('stark-energy-monitor-card', StarkEnergyMonitorCard);
