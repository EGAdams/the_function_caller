class TestGauge extends HTMLElement {
    constructor() {
      super();
      const shadow = this.attachShadow({ mode: 'open' });
  
      // Create a container for the gauge
      const container = document.createElement('div');
      container.classList.add('gauge-container');
  
      // Append the g-force needle component
      const gForceNeedle = document.createElement('g-force-needle');
      container.appendChild(gForceNeedle);
  
      // Append styles if needed
      const style = document.createElement('style');
      style.textContent = `
        .gauge-container {
          position: relative;
          width: 200px;
          height: 200px;
        }
      `;
  
      shadow.appendChild(style);
      shadow.appendChild(container);
    }
  }
  
  customElements.define('test-gauge', TestGauge);
  