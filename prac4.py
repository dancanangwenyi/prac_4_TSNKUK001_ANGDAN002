#!/usr/bin/python
import spidev
import time
import datetime
import os
import sys
# Open SPI bus
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev() # create spi object
spi.open(0,0)
frequency=1000000
spi.max_speed_hz=frequency

# Define delay between readings
delay = 1
# RPI has one bus (#0) and two devices (#0 & #1)
# function to read ADC data from a channel
def GetData(channel): # channel must be an integer 0-7
 adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
 data = ((adc[1]&3) << 8) + adc[2]
 return data
# function to convert data to voltage level,
# places: number of decimal places needed
def ConvertVolts(data,places):
	volts = (data * 3.3) / float(1023)
	volts = round(volts,places)
	return volts
    
def ConvertTemp(data,places):
    temp = ((data * 330)/float(1023))-50
    temp = round(temp,places)
    return temp

def ConvertLight(data,places):
    light = (data/3.28)*100
    light = round(light,places)
    return light
    
# Define sensor channels
temp_channel = 0
light_channel =1
pot_channel =2
timer = datetime.datetime.now()
def main():
        try:
                while True:
                        # Read the light sensor data
                        light_level = GetData(light_channel)
                        light_volts = ConvertVolts(light_level,2)
                        light_percentage = ConvertLight(light_volts,2)
                        # Read the temperature sensor data
                        temp_level = GetData(temp_channel)
                        temp_volts = ConvertVolts(temp_level,2)
                        temp = ConvertTemp(temp_level,2)
                        
                        # Read the potentiometer sensor data
                        pot_level = GetData(pot_channel)
                        pot_volts = ConvertVolts(pot_level,2)
                        
                        #Time now and elapsed time
                        now = datetime.datetime.now()
                        timee = datetime.time(now.hour, now.minute,now.second)
                        instant = now-timer
                        #elapsed = datetime.time(instant.hour,instant.minute,instant.second)
                        # Print out results
                        
                        print "_________________________________________________________"
                        print("Time      Timer         Pot      Temp      Light")
                        print("{}  {}   {}V   {}C   {}%".format(timee,instant,pot_volts,temp,light_percentage))
                        #print()
                        #print("Light : {} ({}V) {}%".format(light_level,light_volts,light_percentage))
                        #print("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
                        #print("Pot  : {} ({}V)".format(pot_level,pot_volts))
                        # Wait before repeating loop
                        time.sleep(delay)
        except KeyboardInterrupt:
                spi.close()
if __name__=="__main__":
    main()
