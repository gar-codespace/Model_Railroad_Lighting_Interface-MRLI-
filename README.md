## Diorama Lighting Automation 
This is the Micropython code for my model railroad layout lighting automation project.  
It's probably suitable for any LED application where granular control and multiple settings are required.  
I think this project would also be suitable for fish and reptile lighting when the project is synced to a real world clock.  
The code runs on a Rasberry Pi Pico or Pico 2.  
  
## Features
This program creates lighting effects suitable for a model railroad or diorama.  
It controls 5 banks of rgbwc LEDs and controls the on or off value of the layouts scenic lights.  
There is also an audio module that is used for ambient sounds.  
This is a stand-alone project, it does not utilize the WiFi feature of the Pico.  
This program controls strip leds, not individually programmible led strips.  

## Lighting Effects  
Different types of animated lighting effects can be defined.  
When run, the effect moves from waypoint to waypoint.  
At the last waypoint, the effect loops and begins again at the first waypoint.  
A waypoint is similar to what a keyframe is in cartoon animation.  
Each color changes from waypoint to waypoint in a linear manner, there is no 
'ease in' or 'ease out' like there is in cartoon animation.  
Even though all effects are animated, some have only one waypoint and thus 
their values do not change over time. This type of effect is considered 
a STATIC effect. Effects with more than one waypoint are considered ANIMATED effects.  

## Static Lighting Effects  
The values for static lighting effects can be changed by the user. The changes are stored
in the STATIC_BUFFER and so are good only as long as the power is on. Permanent changes to the lighting
parameters require editing the dictionaries in the entities file.    
  
## Animated Lighting Effects  
The values of an animated effect can not be changed by the user at the front panel.  
Changes to an animated effect are made by editing the appropriate effect dictionary in the entities file.  
As mentioned, an animated effect moves from waypoint to waypoint and at the end loops back to the beginning.  
There is also a RANDOM value in the effects definition expressed as a decimal percent.  
This setting will shorten the length of the waypoint by a random ammount. Color cahnges are not effected by the RANDOM value, 
only the waypoint length.   
  
## Hardware  
Raspberry Pi Pico or Pico 2  
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
STANDBY - Mutes the display, audio, and RGBWC lights.  The effect is not paused.  

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
  
UASYNCIO:  
https://www.digikey.com/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c  
  
Rotary Encoder Library:  
https://github.com/TTitanUA/micropython_rotary_encoder/tree/main  
  
OLED Display Library:  
https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py  
https://github.com/CrispStrobe/sh1106-py  
  
Button library:  
https://github.com/ubidefeo/MicroPython-Button  
  
## License
The scripts included in this program are © 2026 Greg Ritacco.  
Other then that, there are no restrictions on use.  