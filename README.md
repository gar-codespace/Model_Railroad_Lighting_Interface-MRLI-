## Model Railroad Layout Lighting Automation 
This is the Micropython code for my layout lighting automation.  
It's probably suitable for any led application where granular control and multiple settings are required.  
The code runs on a Rasberry Pi Pico.  

## Features
This program creates lighting effects suitable for a model railroad.  
It controls 5 banks of rgbwc leds at 12 volts and controls the on or off value of the layouts scenic lights.  
There is also an audio module that is used for ambient sounds.  
This is a stand alone project, it does not utilize the WiFi feature of the Pico.  
This program controls strip leds, not individually programmible led strips.  

## Methodology  
There are two types of lighting effects: static and animated.  
For static lighting effects, the asyncio loops run 1 cycle to set the color values and exit.  
For animated lighting effects, the pwm step increment is held constant
and the delay value is set for each color. The delay value of the asyncio loop is different for each color and does not change for the duration of the loop.  
The pwm color change step is constant for all colors.  

## Hardware  
Raspberry Pi Pico 2  
Generic display module (Amazon: AITRIP 1PCS 0.96 Inch OLED Display Module with Buttons EC11 Rotary Encoder IIC Interface LCD Screen Compatible with Arduino(White Color))  
Power Converter (Amazon: DC to DC Power Converter Buck Module 12V 16V (8V to 22V) Buck to 3.3V 2A 3A Max IP67 Waterproof with Overcurrent Overheat Short-Circuit Undervoltage Protection )  
Adafruit STEMMA Analog SPDT Switch - MAX4544 12V - JST PH 2mm  
Adafruit Stereo 20W Class D Audio Amplifier - MAX9744  
Plugs, switches, buttons etc. 

## Operation  
The machine operates in one of 4 modes:  
AUTOMATIC - The display shows a menu of available lighting effects.  
MONITOR - The display shows the values of the 5 colors as the effect progresses.  
MANUAL - The display shows the menu of the 5 colors and their current value.  
ADJUST - The display shows the value of the selected color as it's being adjusted.  

## Navigation  
In Automatic mode:  
  Rotate to scroll through the available lighting effects.  
  Single click to start the hilighted effect.  
  Double click to enter manual mode.  
In Monitor mode:  
  Rotate does nothing.  
  Single click to return to Automatic mode.  
  Double click does nothing. Maybe it should enter Adjust mode for static effects.  
Manual mode:  
  Rotate highlights a different color.  
  Single click selects the hilighted color to adjust.  
  Double click to return to Automatic mode.    
Adjust mode:  
  Rotate to adjust the color value.  
  Single click to accept the adjusted color and return to Manual mode.  
  Double click does nothing.  

## Third Party Developers
Thank you!  

ASYNCIO:  
https://www.digikey.com/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c  

Rotary Encoder Library:  
https://github.com/TTitanUA/micropython_rotary_encoder/tree/main  

OLED Display Library:  
https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py  
   
Button library:  
https://github.com/ubidefeo/MicroPython-Button  

MAX9744 soundcard:  
https://github.com/adafruit/Adafruit_Python_MAX9744  


## License
The scripts included in this program are © 2026 Greg Ritacco.  
Other then that, there are no restrictions on use.  