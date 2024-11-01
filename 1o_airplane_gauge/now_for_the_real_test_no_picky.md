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
    <title>Aircraft G-Force Gauge</title>
    <!-- Include the canvas-gauges library -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-gauges@2.1.7/gauge.min.js"></script>
    <style>
        body {
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        test-gauge {
            width: 400px;
            height: 400px;
        }
    </style>
</head>
<body>
    <test-gauge></test-gauge>

    <script>
        // CoreMotionDataSimulator class
        class CoreMotionDataSimulator {
            constructor(callback) {
                this.callback = callback;
                this.gForce = -2;
                this.intervalId = null;
                this.direction = 1; // 1 for increasing, -1 for decreasing
            }

            start() {
                this.intervalId = setInterval(() => {
                    // Simulate G-force changes between -2g and +2g
                    if (this.gForce >= 2) this.direction = -1;
                    if (this.gForce <= -2) this.direction = 1;
                    this.gForce += 0.1 * this.direction;

                    this.callback(parseFloat(this.gForce.toFixed(1)));
                }, 100);
                // Update every 100ms
            }

            stop() {
                clearInterval(this.intervalId);
            }
        }

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
                            width: 100%;
                            height: 100%;
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
                        { from: -2, to: -1, color: 'rgba(255, 0, 0, .5)' },
                        { from: -1, to: -0.5, color: 'rgba(255, 165, 0, .5)' },
                        { from: -0.5, to: 0.5, color: 'rgba(0, 255, 0, .5)' },
                        { from: 0.5, to: 1, color: 'rgba(255, 165, 0, .5)' },
                        { from: 1, to: 2, color: 'rgba(255, 0, 0, .5)' }
                    ],
                    valueInt: 1,
                    valueDec: 1,
                    colorPlate: '#1a1a1a',
                    colorMajorTicks: '#fff',
                    colorMinorTicks: '#ddd',
                    colorNumbers: '#eee',
                    colorNeedle: 'rgba(255, 69, 0, 1)',
                    colorNeedleEnd: 'rgba(255, 140, 0, 1)',
                    animationDuration: 150,
                    animationRule: 'linear',
                    needleType: 'arrow',
                    needleWidth: 3,
                    borders: false,
                    borderShadowWidth: 0,
                    valueBox: false,
                    colorNeedleCircleOuter: '#fff',
                    needleCircleSize: 7,
                    needleCircleOuter: true,
                    needleCircleInner: false,
                    fontNumbersSize: 24,
                    fontNumbersStyle: 'bold',
                    fontNumbers: 'Roboto',
                    animationTarget: 'plate',
                    animatedValue: true
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
    </script>
</body>
</html>
```

# The Next Step in building our Speedometer Gauge
The preceeding JavaScript System is shows a speedometer that has a needle moving around a gauge like most gauges do.  This needle represents the G-Force of the aircraft.  We need a secondary green needle that is a little less than half the length of the red G-Force needle.  This Green needle will measure speed in mph.

# Your Task
DO NOT WRITE ANY CODE YET.  Just think about how we could achieve putting a primary AND a secondary needle in the same TestGauge space.  If this isn't possible with the gauge library, then let me know what we could do instead.  Make sure that what we are building represents a real-world, Boeing style airplane gauge.  Our customer is extremely picky.  He wants everthing to look JUST LIKE BOEING all the way down to the meticulously drawn tick marks and gauge fonts.  Don't give me more than one solution, just give me the one that you think would be best so that we can make this as professional as possible using only free open-source software.

Go ahead, knock it out of the park. Get creative if you have to.  Make it fun man.
Make sure to put the solution into ONLY ONE HTML code block.  Having to copy only one block of code will save us tons of time.  Remember that efficiency is very important when we are trying to build professional products with limited resources.

