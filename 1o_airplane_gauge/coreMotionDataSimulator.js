export class CoreMotionDataSimulator {
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
  