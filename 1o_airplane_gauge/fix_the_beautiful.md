# Persona
- World-class Python Developer and avid user of GoF Design patterns mixed with Functional Programming whenever it would be more efficient for us to use.

# Our goal
- Build a speedometer for an aircraft with no GPS available,

# Existing Source Code
Here is the code that is supposed to show a gauge for the iOS speedometer that we are building.
```javascript
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>G-Force Gauge Test</title>
    <!-- Include the canvas-gauges library -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-gauges@2.1.7/gauge.min.js"></script>
</head>
<body>
    <test-gauge></test-gauge>

    <script>
        class TestGauge extends HTMLElement {
            constructor() {
                super();
                this.attachShadow({ mode: 'open' });

                // Create template
                const template = document.createElement('template');
                template.innerHTML = `
                    <style>
                        :host {
                            display: block;
                            width: 400px;
                            height: 400px;
                            position: relative;
                        }
                        canvas {
                            width: 100%;
                            height: 100%;
                        }
                    </style>
                    <canvas></canvas>
                `;
                this.shadowRoot.appendChild(template.content.cloneNode(true));

                this.canvas = this.shadowRoot.querySelector('canvas');

                // Initialize the gauge using canvas-gauges
                this.gauge = new RadialGauge({
                    renderTo: this.canvas,
                    width: 400,
                    height: 400,
                    minValue: -2,
                    maxValue: 2,
                    majorTicks: ['-2', '-1', '0', '1', '2'],
                    minorTicks: 10,
                    ticksAngle: 180,
                    startAngle: 90,
                    strokeTicks: true,
                    highlights: [
                        { from: -2, to: -1, color: 'rgba(200, 50, 50, .75)' },
                        { from: -1, to: -0.5, color: 'rgba(200, 200, 50, .75)' },
                        { from: -0.5, to: 0.5, color: 'rgba(50, 200, 50, .75)' },
                        { from: 0.5, to: 1, color: 'rgba(200, 200, 50, .75)' },
                        { from: 1, to: 2, color: 'rgba(200, 50, 50, .75)' }
                    ],
                    valueInt: 1,
                    valueDec: 1,
                    colorPlate: '#fff',
                    colorMajorTicks: '#000',
                    colorMinorTicks: '#000',
                    colorNumbers: '#000',
                    colorNeedle: 'rgba(255, 0, 0, 1)',
                    colorNeedleEnd: 'rgba(255, 0, 0, 1)',
                    animationDuration: 150,
                    animationRule: 'linear',
                    needleType: 'arrow',
                    needleWidth: 3,
                    borders: false,
                    borderShadowWidth: 0,
                    valueBox: false
                }).draw();

                // Start the simulator
                this.simulator = new CoreMotionDataSimulator((value) => {
                    this.gauge.value = value;
                });
                this.simulator.start();
            }

            disconnectedCallback() {
                this.simulator.stop();
            }
        }
        customElements.define('test-gauge', TestGauge);

        // CoreMotionDataSimulator class
        class CoreMotionDataSimulator {
            constructor(callback) {
                this.callback = callback;
                this.gForce = -2;
                this.intervalId = null;
                this.direction = 1;
                // 1 for increasing, -1 for decreasing
            }

            start() {
                this.intervalId = setInterval(() => {
                    // Simulate G-force changes between -2g and +2g
                    if (this.gForce >= 2) this.direction = -1;
                    if (this.gForce <= -2) this.direction = 1;
                    this.gForce += 0.1 * this.direction;

                    this.callback(this.gForce.toFixed(1));
                }, 100);
                // Update every 100ms
            }

            stop() {
                clearInterval(this.intervalId);
            }
        }
    </script>
</body>
</html>
```

# The Problem
The preceeding JavaScript System is causing this JavaScript error:
```error
Uncaught ReferenceError: Cannot access 'CoreMotionDataSimulator' before initialization
    at new TestGauge (index.html:76:38)
    at index.html:86:24
```

# Your Task
Use the JavaScript code below as an inspiration to fix the error in the Problem Section above.
```javascript
<!DOCTYPE html>
<html>
<head>
  <title>My Web App</title>
</head>
<body>
  <script src="simulator.js"></script>  <!-- Include the simulator file first -->
  <script>
    // Your code that uses CoreMotionDataSimulator
    // ...
    this.simulator = new CoreMotionDataSimulator((value) => {
        this.gauge.value = value;
    });
    this.simulator.start();
    // ...
  </script>
</body>
</html>
```

Also, review all of the code when you are done writing it and make sure that of course the error is fixed, but also that there are not any inefficiencies going about.  Make sure that what we are building represents a real-world, Boeing style airplane gauge with whatever library that you think is best.  Don't give me more than one solution, just give me the one that you think would be best so that we can make this as professional as possible using only free open-source software.

Go ahead, knock it out of the park. Get creative if you have to.  make it fun man.
Make sure to put the solution into ONLY ONE HTML code block.  Having to copy only one block of code will save us tons of time.  Remember that efficiency is very important when we are trying to build professional products with limited resources.