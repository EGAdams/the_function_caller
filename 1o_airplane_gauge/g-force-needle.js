class GForceNeedle extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
  
      // Initial angle
      this.angle = 0;
  
      // Create the needle element
      const needle = document.createElement('div');
      needle.classList.add('needle');
  
      // Apply styles
      const style = document.createElement('style');
      style.textContent = `
        .needle {
          position: absolute;
          width: 2px;
          height: 90px;
          background: red;
          top: 10px;
          left: 50%;
          transform-origin: bottom center;
          transform: rotate(${this.angle}deg) translateX(-50%);
          transition: transform 0.1s ease-out;
        }
      `;
  
      this.shadowRoot.append(style, needle);
      this.needleElement = needle;
    }
  
    setAngle(angle) {
      this.angle = angle;
      this.needleElement.style.transform = `rotate(${this.angle}deg) translateX(-50%)`;
    }
  }
  
  customElements.define('g-force-needle', GForceNeedle);
  