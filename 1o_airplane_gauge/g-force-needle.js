// g-force-needle.js

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
        background: linear-gradient(to bottom, #ff0000 0%, #800000 100%);
        top: 50%;
        left: 50%;
        transform-origin: bottom center;
        transform: translate(-50%, -100%) rotate(${this.angle}deg);
        transition: transform 0.1s ease-out;
      }
      .center-cap {
        position: absolute;
        width: 10px;
        height: 10px;
        background: #ff0000;
        border-radius: 50%;
        top: calc(50% - 5px);
        left: calc(50% - 5px);
        z-index: 10;
      }
    `;

    // Create center cap
    const centerCap = document.createElement('div');
    centerCap.classList.add('center-cap');

    this.shadowRoot.append(style, needle, centerCap);
    this.needleElement = needle;
  }

  setAngle(angle) {
    this.angle = angle;
    this.needleElement.style.transform = `translate(-50%, -100%) rotate(${this.angle}deg)`;
  }
}

customElements.define('g-force-needle', GForceNeedle);
