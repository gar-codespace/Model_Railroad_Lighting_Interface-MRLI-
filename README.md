## Diorama Lighting Automation 
This is the Micropython code for my model railroad layout lighting automation project.  
It's probably suitable for any LED application where granular control and multiple settings are required.  
I think this project would also be suitable for fish and reptile lighting when the project is synced to a real world clock.  
The code runs on a Rasberry Pi Pico or Pico 2.  
  
## Features
This program creates lighting effects suitable for a model railroad or diorama.  
It controls 5 banks of rgbwc leds at 12 volts and controls the on or off value of the layouts scenic lights.  
There is also an audio module that is used for ambient sounds.  
This is a stand-alone project, it does not utilize the WiFi feature of the Pico.  
This program controls strip leds, not individually programmible led strips.  
There are two types of lighting effects: static and animated.  
  
## Static Lighting Effects  
For static lighting effects, there is no asyncio loop.  
The values for the RGBWC colors are constant.  
The on or off value for each led bank is constant.  
The values for static lighting effects can be changed by the user. The changes are stored
in a buffer and so are good only as long as the power is on. Permanent changes to the lighting
parameters require editing the dictionaries in the entities file.    
  
## Animated Lighting Effects  
For animated lighting effects, the asyncio delay value is set as a constant.   
  
## Hardware  
Raspberry Pi Pico 2  
Generic display module (Amazon: AITRIP 1PCS 0.96 Inch OLED Display Module with Buttons EC11 Rotary Encoder IIC Interface LCD Screen Compatible with Arduino(White Color))  
Generic display module (Amazon: 1.3 inch White OLED Display Screen Combined with EC11 Rotary Encoder Module IIC Interface for arduino)  
Power Converter (Amazon: DC to DC Power Converter Buck Module 12V 16V (8V to 22V) Buck to 3.3V 2A 3A Max IP67 Waterproof with Overcurrent Overheat Short-Circuit Undervoltage Protection )  
Adafruit STEMMA Relay  
Adafruit Stereo 20W Class D Audio Amplifier - MAX9744  
Plugs, switches, buttons etc. 
  
## Operation  
The machine operates in one of 6 modes:  
WELCOME - The initial screen presented at startup.  
EFFECTS - Displays a scrollable list of available lighting effects.  
ANIMATED - Displays the values of the RGBWC colors as they change.  
STATIC - Displays a selectable list of the RGBWC colors.  
EDIT - Changable value of the selected color.  
STANDBY - Mutes the display, audio, and RGBWC lights.   

## Navigation  
In Welcome mode:  
  
In Effects mode:  
  
In Animated mode:  
  
In Static mode:  
  
in Edit mode:  
  
In Standby mode:  
  
 
## Third Party Developers
Thank you for providing these libraries.    
They have been lightly edited to fit within the schema of this program.  
  
ASYNCIO:  
https://www.digikey.com/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c  
  
Rotary Encoder Library:  
https://github.com/TTitanUA/micropython_rotary_encoder/tree/main  
  
OLED Display Library:  
https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py  
https://github.com/CrispStrobe/sh1106-py  
  
Button library:  
https://github.com/ubidefeo/MicroPython-Button  
  
MAX9744 soundcard:  
  
  
## License
The scripts included in this program are © 2026 Greg Ritacco.  
Other then that, there are no restrictions on use.  