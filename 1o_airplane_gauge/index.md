# Persona
- World-class javascript developer
- Expert GoF user
- 30 years of experience desiging software that uses iOS Core Motion data to determine speed without GPS
- Seasoned Vanilla JavaScript WebComponent Developer

# Your Task
Help me create

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>G-Force Needle Test</title>
  <script>
    class CoreMotionDataSimulator {
    constructor(callback) {
      this.callback = callback;
      this.gForce = 0;
      this.intervalId = null;
      this.direction = 1; // 1 for increasing, -1 for decreasing
    }
  
    start() {
      this.intervalId = setInterval(() => {
        // Simulate G-force changes between -2g and +2g
        if (this.gForce >= 2) this.direction = -1;
        if (this.gForce <= -2) this.direction = 1;
        this.gForce += 0.1 * this.direction;
  
        // Map G-force to angle (assuming -2g to +2g maps to -90deg to +90deg)
        const angle = (this.gForce / 2) * 90;
  
        this.callback(angle);
      }, 100); // Update every 100ms
    }
  
    stop() {
      clearInterval(this.intervalId);
    }
  }
  </script>
  <script>
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
  
  </script>
  <script>
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
  </script>
</head>
<body>
  <test-gauge></test-gauge>

  <script>

    // Wait for the custom elements to be defined
    window.addEventListener('DOMContentLoaded', () => {
      const testGauge = document.querySelector('test-gauge');
      const gForceNeedle = testGauge.shadowRoot.querySelector('g-force-needle');

      // Instantiate the simulator
      const simulator = new CoreMotionDataSimulator((angle) => {
        // Update the needle's angle
        gForceNeedle.setAngle(angle);
      });

      // Start the simulation
      simulator.start();
    });
  </script>
</body>
</html>
