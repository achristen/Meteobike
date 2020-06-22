#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Program <meteobike_epaper.py> to read and record GPS data, air temperature and humidity
using Adafruit's Ultimate GPS and Pimoroni's DHT22 temperature sensor while riding
on a bike. This version will display data on E-paper instead of on-screen.
Developed by: University of Freiburg
Chair of Environmental Meteology, meteo@meteo.uni-freiburg.de
Version 1.40 - EPAPER VERSION
Written by Heinz Christen Mar 2018 
Modified by Andreas Christen Apr 2018, May 2019, Jun 2020
Modified by Kostas Politakos Mar 2020
Using the class GpsPoller written by Dan Mandle http://dan.mandle.me September 2012 License: GPL 2.0
For detailed description see: https://github.com/achristen/Meteobike/
"""
from __future__ import division
import socket
import importlib
import math
from io import StringIO
import csv
import time
import os,sys
import logging
sys.path.insert(1,'/home/pi/e-Paper/RaspberryPi&JetsonNano/python/lib')
from waveshare_epd import epd2in7b
from PIL import Image,ImageDraw,ImageFont
import traceback
import datetime
from datetime import timedelta
from gps import *
import Adafruit_DHT
import threading
from Tkinter import *
from time import gmtime, strftime
import numpy
import socket
import RPi.GPIO as GPIO

#User ID & Constants
raspberryid = "52" # enter your raspberry's number
studentname = "Andreas" # enter your first name - no spaces and no special characters
temperature_cal_a1 = 1.00000 # enter the calibration coefficient slope for temperature
temperature_cal_a0 = 0.00000 # enter the calibration coefficient offset for temperature
vappress_cal_a1 = 1.00000 # enter the calibration coefficient slope for vapour pressure
vappress_cal_a0 = 0.00000 # enter the calibration coefficient offset for vapour pressure

#Creating Data File
display_interval = 5 # display epaper every X records
logfile_path = "/home/pi/Desktop/"
logfile = logfile_path+raspberryid+"-"+studentname+"-"+strftime("%Y-%m-%d.csv") # construct file name 

#Retrieve IP from system
def get_ip():#gives the ip adress of our unique RaspberryPi
         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         try:
             # doesn't even have to be reachable
             s.connect(('10.255.255.255', 1))
             IP = s.getsockname()[0]
         except:
             IP = '127.0.0.1'
         finally:
             s.close()
         return IP

#Counter 
cnt = 0 #Starting value
def counter(): #Every time we record data, the cnt is increased by one
     global cnt
     cnt+=1
     return cnt

# setting global variables
gpsd = None
class GpsPoller(threading.Thread):
   def __init__(self):
     threading.Thread.__init__(self)
     global gpsd # bring it in scope
     gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
     self.current_value = None
     self.running = True # setting the thread running to true
   def run(self):
     global gpsd
     while gpsp.running:
       gpsd.next() # this will continue to loop and grab EACH set of gpsd info to clear the buffer
gpsp = GpsPoller() # create the thread
gpsp.start() # start it up

#Recognizing status for speed
def gps():
     has_fix=False#assume no fix
     f_mode=int(gpsd.fix.mode)#store number of sats
     global gps_count
     if f_mode > 2 :#True if we have a GPS signal
         has_fix=True
         if cnt==0: #If have a GPS signal from the 1st running
             gps_count=0
         if gps_count==1:# Gps on for 2*n times
             gps_count=2
         elif gps_count==2:# Gps on for 2*(n+1/2)times
             gps_count=1
         if gps_count==0:#  Gps on for 1st time
             gps_count=1
     else:
         gps_count=0

     return gps_count

#Initiative status - Recording
status_record="on"
recording = True

sampling_rate = 5 # sampling rate - minimum number of seconds between samplings

dht22_pin = 4 # pin for DHT22 Data
dht22_sensor = Adafruit_DHT.DHT22

#callback functions
def exit_program():
         sys.exit()
def record_data():
         global recording
         recording=True
         global status_record
         status_record="On"
         if os.path.isfile(logfile):return
         else:#write header line
                 f0=open(logfile,"w")
                 f0.write("ID,Record,Raspberry_Time,GPS_Time,Altitude,Latitude,Longitude,Temperature,TemperatureRaw,RelHumidity,RelHumidityRaw,VapourPressure,VapourPressureRaw,Velocity\n")
                 f0.close()
def stop_data():
         global recording
         recording=False
         global status_record
         status_record="Off"

#Main Program
record_data() #Always Recording at the beginning

while True:    
     def count():
         #Initiative Imports & Modules
         from waveshare_epd import epd2in7b
         from PIL import Image,ImageDraw,ImageFont
         import traceback
         datetimeFormat='%Y-%m-%d %H:%M:%S'
         rad_Earth=6378100.0
         computer_time = strftime("%Y-%m-%d %H:%M:%S")

         #Gps Variables
         gps_time=gpsd.utc
         gps_altitude=gpsd.fix.altitude
         gps_latitude=gpsd.fix.latitude
         gps_longitude=gpsd.fix.longitude
         gps_on=gps()#Checking for Gps Signal
         f_mode=int(gpsd.fix.mode) #store number of sats
         has_fix=False
         if f_mode > 2 :
             has_fix=True
         if has_fix==True and gps_on==1:
             global lat1,lon1,rho1,z1,x1,y1,t1
             lat1=math.pi*gps_latitude/180.0
             lon1=math.pi*gps_longitude/180.0
             rho1=rad_Earth*math.cos(lat1)
             z1=rad_Earth*math.sin(lat1)
             x1=rho1*math.cos(lon1)
             y1=rho1*math.sin(lon1)
             t1=computer_time
         if has_fix==True and gps_on==2:
             global lat2,lon2,rho2,z2,x2,y2,t2,dot,cos_theta,theta,dist,t2,vel
             lat2=math.pi*gps_latitude/180.0
             lon2=math.pi*gps_longitude/180.0
             rho2=rad_Earth*math.cos(lat2)
             z2=rad_Earth*math.sin(lat2)
             x2=rho2*math.cos(lon2)
             y2=rho2*math.sin(lon2)
             dot=(x1*x2+y1*y2+z1*z2)
             cos_theta=dot/(rad_Earth*rad_Earth)
             if cos_theta < 1 and cos_theta > -1:
                theta=math.acos(cos_theta)
             else: theta=float("nan")
             dist=rad_Earth*theta
             t2=computer_time
             diff=datetime.datetime.strptime(t2,datetimeFormat)-datetime.datetime.strptime(t1,datetimeFormat)
             vel=dist/diff.seconds
             lat1=lat2
             lon1=lon2
             rho1=rho2
             z1=z2
             x1=x2
             y1=y2
             t1=t2
             gps()

         #Calculating Variables
         dht22_humidity, dht22_temperature = Adafruit_DHT.read_retry(dht22_sensor, dht22_pin)
         dht22_temperature_raw=round(dht22_temperature,5)
         dht22_temperature_calib=round(dht22_temperature * temperature_cal_a1 + temperature_cal_a0,3)
         dht22_temperature = dht22_temperature_calib
         saturation_vappress_ucalib = 0.6113 * numpy.exp((2501000.0/461.5)*((1.0/273.15)-(1.0/(dht22_temperature_raw+273.15))))
         saturation_vappress_calib = 0.6113 * numpy.exp((2501000.0/461.5)*((1.0/273.15)-(1.0/(dht22_temperature_calib+273.15))))
         dht22_vappress=(dht22_humidity/100.0)*saturation_vappress_ucalib
         dht22_vappress_raw=round(dht22_vappress,5)
         dht22_vappress_calib=round(dht22_vappress * vappress_cal_a1 + vappress_cal_a0,5)
         dht22_vappress = dht22_vappress_calib
         dht22_humidity_raw=round(dht22_humidity,3)
         dht22_humidity = round(100 * (dht22_vappress_calib / saturation_vappress_calib),3)
         if dht22_humidity >100:dht22_humidity=100
         
         if cnt == 0:
             global temperature_prev,humidity_prev,vappress_prev
             temperature_prev = 0
             humidity_prev = 0
             vappress_prev = 0
             
         tendency_temperature = dht22_temperature - temperature_prev
         tendency_humidity = dht22_humidity - humidity_prev
         tendency_vappress = dht22_vappress - vappress_prev
         
         if cnt % 5 == 0:
            temperature_prev = dht22_temperature
            humidity_prev = dht22_humidity
            vappress_prev = dht22_vappress
         
         #ePaper Begins
         epd = epd2in7b.EPD()
         epd.init()

         #Font Description 
         font_dir='/home/pi/e-Paper/RaspberryPi&JetsonNano/python/pic'
         font18 = ImageFont.truetype(os.path.join(font_dir, 'Font.ttc'), 18)
         font14 = ImageFont.truetype(os.path.join(font_dir, 'Font.ttc'), 14)

         left_spacing = 3
         first_line = 4
         last_line = 255
         line_spacing_18 = 23
         line_spacing_14 = 16

         #Descriptive image 
         if cnt == 0:#1st run
             
             print('Hello '+studentname+', Welcome to Meteobike #'+raspberryid)
             
             LBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
             LRedimage= Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
             
             drawblack = ImageDraw.Draw(LBlackimage)
             drawred = ImageDraw.Draw(LRedimage)
             
             drawblack.text((4, 4),  'Hello '+studentname, font = font18, fill = 0)
             drawblack.text((4, 40),  'Meteobike #'+raspberryid , font = font14, fill = 0)
             if get_ip()=='127.0.0.1':
               drawred.text((4,55), 'No WiFi connection', font = font14, fill = 0)
             else: drawblack.text((4,55), 'IP: ' +get_ip(), font = font14, fill = 0)   
             
             drawblack.text((4, 90),  'Key 1: Pause Recording' , font = font14, fill = 0)
             drawblack.text((4, 105), 'Key 2: Resume Recording' , font = font14, fill = 0)
             drawblack.text((4, 120), 'Key 4: Exit Recording' , font = font14, fill = 0)
             drawblack.text((4, 180), 'Hold keys for 2 seconds.', font = font14, fill = 0)  
             drawred.text((4, 200), 'Your Meteobike will \nstart automatically now \nif you press no key.', font = font14, fill = 0)  
             epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))
             time.sleep(8)

         if recording == True:#cnt+1
             counter()

         # Data Recording
         if recording:# and has_fix: it depends
             f0=open(logfile,"a")
             f0.write(raspberryid+",")
             f0.write(str(cnt)+",")
             f0.write(computer_time+",")
             if has_fix:f0.write(gps_time+",")
             else:f0.write("nan,")
             f0.write("{0:.3f}".format(gps_altitude)+",")
             f0.write("{0:.6f}".format(gps_latitude)+",")
             f0.write("{0:.6f}".format(gps_longitude)+",")
             f0.write(str(dht22_temperature)+",")
             f0.write(str(dht22_temperature_raw)+",")
             f0.write(str(dht22_humidity)+",")
             f0.write(str(dht22_humidity_raw)+",")
             f0.write(str(dht22_vappress)+",")
             f0.write(str(dht22_vappress_raw)+",")
             if has_fix==True and gps_on==2:f0.write(str(vel)+"\n")
             else:f0.write("nan\n")
             f0.close()
                   
        # ---------------------------------
        # E-Paper 
        # ---------------------------------        
           
         #Measurement Screen
        
         LBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the fram
         LRedimage= Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame

         drawblack = ImageDraw.Draw(LBlackimage)
         drawred = ImageDraw.Draw(LRedimage)
         
         arrow_temperature = '' 
         if tendency_temperature > 0 and cnt > 1:
          arrow_temperature = u'↑'
         if tendency_temperature < 0 and cnt > 1:
          arrow_temperature = u'↓'
         if tendency_temperature == 0 and cnt > 1:
          arrow_temperature = u'→'
         
         arrow_humidity = '' 
         if tendency_humidity > 0 and cnt > 1:
          arrow_humidity = u'↑'
         if tendency_humidity < 0 and cnt > 1:
          arrow_humidity = u'↓'
         if tendency_humidity == 0 and cnt > 1:
          arrow_humidity = u'→'
         
         arrow_vappress = '' 
         if tendency_vappress > 0 and cnt > 1:
          arrow_vappress = u'↑'
         if tendency_vappress < 0 and cnt > 1:
          arrow_vappress = u'↓'
         if tendency_vappress == 0 and cnt > 1:
          arrow_vappress = u'→'
                    
         if gpsd.fix.latitude < 0:
           latitude_ns = "S"   
         else: latitude_ns = "N"        
         if gpsd.fix.longitude < 0:
           longitude_ew = "W"   
         else: longitude_ew = "E"  
                    
         drawblack.text((left_spacing,first_line+0*line_spacing_18), 'T: ' +"{0:.1f}".format(dht22_temperature)+u'°C '+arrow_temperature, font = font18, fill = 0)
         drawblack.text((left_spacing,first_line+1*line_spacing_18), 'RH: '+"{0:.1f}%".format(dht22_humidity)+' '+arrow_temperature, font = font18, fill = 0)
         drawblack.text((left_spacing,first_line+2*line_spacing_18), 'Vap.Prs.: '+"{0:.2f} kPa".format(dht22_vappress)+' '+arrow_vappress, font = font18, fill = 0) 
         if has_fix==True and gps_on==2: #presents Velocity if available
             drawblack.text((left_spacing,first_line+3*line_spacing_18), 'Speed: ' +"{0:.1f} m/s".format(vel), font = font18, fill= 0)
         else:drawred.text((left_spacing,first_line+3*line_spacing_18), 'Error: No GPS Signal', font = font18, fill = 0)
         if has_fix==True and gps_on==2:
             drawblack.text((left_spacing,first_line+10+3*line_spacing_18+1*line_spacing_14), 'Altitude: ' +"{0:.1f} m".format(gpsd.fix.altitude), font = font14, fill = 0)
             drawblack.text((left_spacing,first_line+10+3*line_spacing_18+2*line_spacing_14), 'Pos.: ' +"{0:.3f}".format(abs(gpsd.fix.latitude))+u'°'+latitude_ns+'/'+"{0:.3f}".format(abs(gpsd.fix.longitude))+u'°'+longitude_ew, font = font14, fill = 0)
             drawblack.text((left_spacing,first_line+10+3*line_spacing_18+3*line_spacing_14), 'Date: ' +gps_time[0:10], font = font14, fill = 0)
             drawblack.text((left_spacing,first_line+10+3*line_spacing_18+4*line_spacing_14), 'Time: ' +gps_time[11:19]+' UTC', font = font14, fill = 0)
         
         drawblack.line((left_spacing, 170, epd.width-left_spacing, 170), fill = 0)
         drawblack.text((left_spacing,last_line-5*line_spacing_14), studentname+"'s Meteobike", font = font14, fill = 0)
         drawblack.text((left_spacing,last_line-4*line_spacing_14), 'Meteobike #' +raspberryid, font = font14, fill = 0)
         if get_ip()=='127.0.0.1':
             drawred.text((left_spacing,last_line-3*line_spacing_14), 'No WiFi connection', font = font14, fill = 0)
         else: drawblack.text((left_spacing,last_line-3*line_spacing_14), 'IP: ' +get_ip(), font = font14, fill = 0)   
         if status_record=="On" and has_fix==True and gps_on==2:
             drawblack.text((left_spacing,last_line-2*line_spacing_14), 'Recording : On', font = font14, fill = 0)
         else: drawred.text((left_spacing,last_line-2*line_spacing_14), 'Recording: Off', font = font14, fill = 0)
         drawblack.text((left_spacing,last_line-1*line_spacing_14), 'Record No: '+str(cnt), font = font14, fill = 0)
         if cnt % display_interval == 0:
            epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))
         if cnt == 1:
            epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))
            
         #Decision Phase
         t=0
         while True:
             GPIO.setmode(GPIO.BCM)
             key1 = 5
             key2 = 6
             key3 = 13
             key4 = 19
             GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
             GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
             GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
             GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
             '''2Gray(Black and white) display'''
             key1state = GPIO.input(key1)
             key2state = GPIO.input(key2)
             key3state = GPIO.input(key3)
             key4state = GPIO.input(key4)
             
             LBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the fram
             LRedimage= Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
             drawblack = ImageDraw.Draw(LBlackimage)
             drawred = ImageDraw.Draw(LRedimage)
             
             drawblack.line((left_spacing, 170, epd.width-left_spacing, 170), fill = 0)
             drawblack.text((left_spacing,last_line-5*line_spacing_14), studentname+"'s Meteobike", font = font14, fill = 0)
             drawblack.text((left_spacing,last_line-4*line_spacing_14), 'Meteobike #' +raspberryid, font = font14, fill = 0)
             if get_ip()=='127.0.0.1':
                 drawred.text((left_spacing,last_line-3*line_spacing_14), 'No WiFi connection', font = font14, fill = 0)
             else: drawblack.text((left_spacing,last_line-3*line_spacing_14), 'IP: ' +get_ip(), font = font14, fill = 0)   
             drawblack.text((left_spacing,last_line-1*line_spacing_14), 'Record No: '+str(cnt), font = font14, fill = 0)
             
             if key1state == False:
                 drawred.text((left_spacing, first_line), 'Recording \npaused' , font = font18, fill = 0)
                 drawred.text((left_spacing,last_line-2*line_spacing_14), 'Recording : Paused', font = font14, fill = 0)
                 epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))
                 print('Key1 Pressed')
                 stop_data()
                 break
             if key2state == False:
                 drawblack.text((left_spacing, first_line), 'Recording started' , font = font18, fill = 0)
                 drawblack.text((left_spacing,last_line-2*line_spacing_14), 'Recording : On', font = font14, fill = 0)
                 epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))
                 print('Key2 Pressed')
                 record_data()
                 break
             if key3state == False:
                 print('Key3 Pressed')
                 break
             if key4state == False:
                 drawred.text((left_spacing, first_line+0*line_spacing_18), 'Meteobike' , font = font18, fill = 0)
                 drawred.text((left_spacing, first_line+1*line_spacing_18), 'stopped' , font = font18, fill = 0)
                 drawblack.text((left_spacing, first_line+10+3*line_spacing_18+1*line_spacing_14), 'To resume logging, you' , font = font14, fill = 0)
                 drawblack.text((left_spacing, first_line+10+3*line_spacing_18+2*line_spacing_14), 'must reboot your system' , font = font14, fill = 0)
                 drawred.text((left_spacing,last_line-2*line_spacing_14), 'Recording : Off', font = font14, fill = 0)
                 epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))
                 print('Key4 Pressed')
                 exit_program()
                 break     
             if t==5:
                 break
             t+=1
             time.sleep(1)

     count()
