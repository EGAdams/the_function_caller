# Persona
You are a word-class JavaScript developer with many years of experience developing software that controls gauges for aircraft using Apple's Core Motion framework.
You are an expert at calculating speed from the Core Motion data.
You are an expert at drawing gauges in JavaScript that go into the WebView of an iOS app.

# Our goal
We are making a Decelerometer for an aircraft.  

# Test Description
The test starts at a full stop, where the speed is zero.
We don't start measuring speed until a start button is pressed and then we start moving forward.  We move forward immediately after pressing the start button, so there is a small delay between pressing the start button and the aircraft moving forward. After we start moving forward, we start measuring speed.  Then we speed up to about 20 mph and then we hit the brakes and slow down to a stop.  We stop measuring speed when we get below 4 mph.  We want to measure speed as accurately as possible by using the accelerometer and rotation matrix from the Core Motion object.

# The display
## Professional Airplane G-Force Gauge Display

We aim to design an advanced airplane gauge that exemplifies the highest standards of precision, elegance, and functionality, adhering to Material Design principles. This gauge will visually represent the G-force of acceleration data sourced from the iOS Core Motion Object. The display should look and feel like it belongs in the cockpit of a premium Boeing aircraft.

### Key Design Elements:
- **Needle for G-Force Measurement**: A meticulously crafted needle, resembling the precision of an analog aircraft instrument, will dynamically point to the real-time G-force. The motion of the needle will be fluid and smooth, ensuring accuracy in representation.
  
- **Digital G-Force Display**: Positioned prominently in the center of the gauge, the G-force value will also be presented as a clear, easy-to-read digital reading. The font will exude a sense of professionalism and clarity, similar to avionics displays used in Boeing cockpits.

- **Speed Scale**: Around the circumference of the gauge, a high-contrast speed scale will be displayed. The numbers will be sharp and easy to distinguish, resembling the clarity and precision expected in a high-class airplane cockpit.

- **Yaw Indicator**: Integrated within the gauge, a secondary yaw indicator will feature a half-circle arc ranging from 9:00 to 3:00. The yaw needle, a short yet sophisticated triangular design, will smoothly pivot within this arc. Despite its minimal height (about four characters), the needle's motion will be smooth and refined, maintaining the premium look of an aircraft's yaw indicator.

- **Material Design Influence**: The entire interface will follow Material Design guidelines, ensuring that the gauge is not only functional but aesthetically pleasing with sleek transitions, subtle shading, and a tactile, high-quality feel. The interface will use a color palette inspired by modern aviation displays—clean whites, deep blacks, and subtle accent colors, ensuring that the gauge is both easy to read and visually striking.

- **Seamless Needle Movement**: Both the G-force and yaw needles will exhibit flawless motion, ensuring a smooth experience as they transition between different measurements. This will mimic the fluidity and precision of a real-world aircraft gauge, reinforcing the premium feel of the display.

This professional gauge will reflect the high standards of a Boeing aircraft, delivering not only precise readings but also a visually captivating, high-class design that elevates the user experience.
"""


# Your Task
We are going to create the html page for now and then we will move it to the iOS WebView after we have tested its operation.  So we will need sampla Core Motion data to test the gauge.  Before we write any code, I want you to break up the proposed system into as many Javascript objects thay you can for the view part.  remember to uses materials design to help us be more professional.  We want to be ablel to creat a testable part of the view first , like the red needle, and than build the other partds after we have tested the simpler one.  Please list the objects that we would need for the view and give me a brief description of each.