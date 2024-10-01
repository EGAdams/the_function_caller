// test-gauge.js

class TestGauge extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: 'open' });

    // Create a container for the gauge
    const container = document.createElement('div');
    container.classList.add('gauge-container');

    // Append the speed scale component
    const speedScale = document.createElement('speed-scale');
    container.appendChild(speedScale);

    // Append the g-force needle component
    const gForceNeedle = document.createElement('g-force-needle');
    container.appendChild(gForceNeedle);

    // Append styles
    const style = document.createElement('style');
    style.textContent = `
      .gauge-container {
        position: relative;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle at center, #2c3e50 0%, #000000 70%);
        border-radius: 50%;
        overflow: hidden;
        box-shadow: inset 0 0 10px #000000;
      }
      speed-scale,
      g-force-needle {
        position: absolute;
        top: 0;
        left: 0;
      }
    `;

    shadow.appendChild(style);
    shadow.appendChild(container);
  }
}

customElements.define('test-gauge', TestGauge);
