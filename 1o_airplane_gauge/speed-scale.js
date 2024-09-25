// speed-scale.js

class SpeedScale extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
  
      // Create the SVG container for the scale
      const svgNS = 'http://www.w3.org/2000/svg';
      const svg = document.createElementNS(svgNS, 'svg');
      svg.setAttribute('viewBox', '0 0 200 200');
      svg.style.width = '100%';
      svg.style.height = '100%';
  
      // Draw the scale markings and numbers
      this.drawScale(svg);
  
      // Append styles if needed
      const style = document.createElement('style');
      style.textContent = `
        text {
          fill: #fff;
          font-size: 12px;
          text-anchor: middle;
          dominant-baseline: middle;
        }
        line {
          stroke: #fff;
          stroke-width: 2;
        }
      `;
  
      this.shadowRoot.append(style, svg);
    }
  
    drawScale(svg) {
      const svgNS = 'http://www.w3.org/2000/svg';
      const centerX = 100;
      const centerY = 100;
      const radius = 90; // Radius for the scale
  
      // Define the scale range and intervals
      const minValue = -2; // -2g
      const maxValue = 2;  // +2g
      const majorTickInterval = 0.5; // Major ticks every 0.5g
      const minorTickInterval = 0.1; // Minor ticks every 0.1g
  
      // Total degrees covered by the scale (-90 to +90 degrees)
      const startAngle = -90;
      const endAngle = 90;
  
      // Draw major and minor ticks
      for (let gForce = minValue; gForce <= maxValue; gForce += minorTickInterval) {
        const angle = this.mapValueToAngle(gForce, minValue, maxValue, startAngle, endAngle);
        const radians = (angle * Math.PI) / 180;
  
        const innerRadius = radius - 10;
        const outerRadius = radius;
  
        const x1 = centerX + innerRadius * Math.cos(radians);
        const y1 = centerY + innerRadius * Math.sin(radians);
        const x2 = centerX + outerRadius * Math.cos(radians);
        const y2 = centerY + outerRadius * Math.sin(radians);
  
        const line = document.createElementNS(svgNS, 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
  
        // Thicker line for major ticks
        if (gForce % majorTickInterval === 0) {
          line.style.strokeWidth = '3';
        } else {
          line.style.strokeWidth = '1';
        }
  
        svg.appendChild(line);
  
        // Add numbers for major ticks
        if (gForce % majorTickInterval === 0) {
          const textRadius = radius - 20;
          const textX = centerX + textRadius * Math.cos(radians);
          const textY = centerY + textRadius * Math.sin(radians);
  
          const text = document.createElementNS(svgNS, 'text');
          text.setAttribute('x', textX);
          text.setAttribute('y', textY);
          text.textContent = gForce.toFixed(1);
  
          svg.appendChild(text);
        }
      }
    }
  
    mapValueToAngle(value, minValue, maxValue, startAngle, endAngle) {
      // Map a value in [minValue, maxValue] to an angle in [startAngle, endAngle]
      const ratio = (value - minValue) / (maxValue - minValue);
      return startAngle + ratio * (endAngle - startAngle);
    }
  }
  
  customElements.define('speed-scale', SpeedScale);
  