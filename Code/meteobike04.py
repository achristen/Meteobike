#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Program <meteobike.py> to read and record GPS data, air temperature and humidity
using Adafruit's Ultimate GPS and Pimoroni's DHT22 temperature sensor while riding
on a bike.
University of Freiburg
Environmental Meteology
Version 1.2
Written by Heinz Christen Mar 2018 
Modified by Andreas Christen Apr 2018 
Using the class GpsPoller
written by Dan Mandle http://dan.mandle.me September 2012 License: GPL 2.0
Buttons:
Record:	Start recording in append mode to logfile, but only if gps has fix
Stop:	Stop recording (Pause)
Exit:	exit program
"""
from __future__ import division
import socket
import importlib
import math
from io import StringIO
import csv
import time
import os,sys
sys.path.insert(1,'/home/pi/Meteobike04/meteobike04')
from waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
import traceback
from UTCI import *
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
cnt = 0 #Starting point
def counter(): #Every time we have recording on the cnt is getting greater by one
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
        print(gps_count)
    else:
        gps_count=0
        
    return gps_count
#User ID & Constants
raspberryid = "02" # enter your raspberry's number
studentname = "kostas" # enter your first name - no spaces and no special characters
temperature_cal_a1 = 1.02598# enter the calibration coefficient slope for temperature
temperature_cal_a0 = -0.470601 # enter the calibration coefficient offset for temperature
vappress_cal_a1 = 1.37302# enter the calibration coefficient slope for vapour pressure
vappress_cal_a0 = -0.654250# enter the calibration coefficient offset for vapour pressure

#Creating Data File
window_title = "Meteobike"+raspberryid
logfile_path = "/home/pi/Desktop/"
logfile = logfile_path+raspberryid+"-"+studentname+"-"+strftime("%Y-%m-%d.csv") # construct file name 
font_size=24

#Initiative status - Recording
status_record="on"
recording = True

sampling_rate = 5 # sampling rate - minimum number of seconds between samplings

dht22_pin = 4 # pin for DHT22 Data
dht22_sensor = Adafruit_DHT.DHT22

#callback functions
def exit_program():
        master.destroy()
        sys.exit()
def record_data():
        global recording
        recording=True
        global status_record
        status_record="on"
        if os.path.isfile(logfile):return
        else:#write header line
                f0=open(logfile,"w")
                f0.write("ID,Record,Raspberry_Time,GPS_Time,Altitude,Latitude,Longitude,Temperature,TemperatureRaw,RelHumidity,RelHumidityRaw,VapourPressure,VapourPressureRaw,Velocity\n")
                f0.close()
def stop_data():
        global recording
        recording=False
        global status_record
        status_record="off"
        
#Main Program
record_data()#Always Recording at the Beggining
while True:    
    def count():
        #Initiative Imports & Modules
        from waveshare_epd import epd2in7
        from PIL import Image,ImageDraw,ImageFont
        import traceback
        datetimeFormat='%Y-%m-%d %H:%M:%S'
        rad_Earth=6378100
        computer_time = strftime("%Y-%m-%d %H:%M:%S")
        
        #Gps Variables
        gps_time=gpsd.utc
        gps_altitude=gpsd.fix.altitude
        gps_latitude=gpsd.fix.latitude
        gps_longitude=gpsd.fix.longitude
        gps_on=gps()#Checking for Gps Signal
        f_mode=int(gpsd.fix.mode)#store number of sats
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
            theta=math.acos(cos_theta)
            dist=rad_Earth*theta
            t2=computer_time
            diff=datetime.datetime.strptime(t2,datetimeFormat)-datetime.datetime.strptime(t1,datetimeFormat)
            #print(diff.seconds)
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
        dht22_vappress_raw=round(dht22_vappress,3)
        dht22_vappress_calib=round(dht22_vappress * vappress_cal_a1 + vappress_cal_a0,3)
        dht22_vappress = dht22_vappress_calib
        dht22_humidity_raw=round(dht22_humidity,5)
        dht22_humidity = round(100 * (dht22_vappress_calib / saturation_vappress_calib),5)
        if dht22_humidity >100:dht22_humidity=100
        
        #ePaper Begins
        epd = epd2in7.EPD()
        epd.init()
        
        #Font Description 
        font24 = ImageFont.truetype(os.path.join('/home/pi/Meteobike04', 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join('/home/pi/Meteobike04', 'Font.ttc'), 18)
        font35 = ImageFont.truetype(os.path.join('/home/pi/Meteobike04', 'Font.ttc'), 35)
        font14 = ImageFont.truetype(os.path.join('/home/pi/Meteobike04', 'Font.ttc'), 14)
             
        #Descriptive image 
        if cnt == 0:#1st run
            Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)
            draw.text((75, 2), ' Choices ' , font = font24, fill = 0)
            draw.text((2, 25), ' Key1: Start Recording ' , font = font18, fill = 0)
            draw.text((2, 45), ' Key2: Stop Recording ' , font = font18, fill = 0)
            draw.text((2, 65), ' Key3: Continue Recording' , font = font18, fill = 0)
            draw.text((2, 85), ' Key4: Exit Recording ' , font = font18, fill = 0)
            draw.text((2, 105), 'If you do not make any choices the \nprogram continues with last preferences.\nEvery time you have five seconds to \ndecide. Press for two seconds.' , font = font14, fill = 0)
            epd.display(epd.getbuffer(Himage))
            time.sleep(10)
            
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
            
        #Measurements    
        Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        draw.text((2, 0), ' Meteobike ' + raspberryid, font = font24, fill = 0)
        draw.text((2,35), 'Ta: ' +"{0:.1f} C".format(dht22_temperature), font = font18, fill = 0)
        draw.text((2,65), 'RH: '+"{0:.1f} %".format(dht22_humidity), font = font18, fill = 0)
        draw.text((2,95), 'Vap_press: '+"{0:.1f} kPa".format(dht22_vappress), font = font18, fill = 0)
        draw.text((2,125), 'Altitude: ' +"{0:.2f} m".format(gpsd.fix.altitude), font = font18, fill = 0)
        draw.text((2,155), 'Latitude: ' +"{0:.2f} N".format(gpsd.fix.latitude), font = font18, fill = 0)
        draw.text((2,185), 'Longitude: ' +"{0:.2f} E".format(gpsd.fix.longitude), font = font18, fill = 0)
        if has_fix==True and gps_on==2: #presents Velocity and gps time
            draw.text((2,205), 'Velocity: ' +"{0:.2f} m/s".format(vel), font = font14, fill= 0)
            draw.text((2,235), 'Gps: ' +gpsd.utc+' ', font = font14, fill = 0)
        else:draw.text((2,235), 'Time: '+computer_time+' ', font = font14, fill = 0)
        draw.text((2,220), 'Recording: ' +status_record+ '  Counter: ' +str(cnt), font = font14, fill = 0)
        draw.text((2,250), 'name: ' +studentname, font = font14, fill = 0)
        #draw.text((2,250), 'IP: ' +get_ip(), font = font14, fill = 0)
        epd.display(epd.getbuffer(Limage))           
        
       
        
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
            if key1state == False:
                record_data()
                Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
                draw = ImageDraw.Draw(Himage)
                draw.text((75, 2), ' Recording \n  Started ' , font = font24, fill = 0)
                epd.display(epd.getbuffer(Himage))
                print('Key1 Pressed')
                break
            if key2state == False:
                stop_data()
                Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
                draw = ImageDraw.Draw(Himage)
                draw.text((75, 2), ' Recording \n  Stopped' , font = font24, fill = 0)
                epd.display(epd.getbuffer(Himage))
                print('Key2 Pressed')
                break
            if key3state == False:
                Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
                draw = ImageDraw.Draw(Himage)
                draw.text((75, 2), ' Recording \n Continues' , font = font24, fill = 0)
                epd.display(epd.getbuffer(Himage))
                print('Key3 Pressed')
                break
            if key4state == False:
                Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
                draw = ImageDraw.Draw(Himage)
                draw.text((75, 2), ' EXIT' , font = font35, fill = 0)
                epd.display(epd.getbuffer(Himage))
                exit_program()
                print('Key4 Pressed')
                break     
            if t==5:
                #Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
                #draw = ImageDraw.Draw(Himage)
                #draw.text((75, 2), ' Recording \n Continues ' , font = font24, fill = 0)
                #epd.display(epd.getbuffer(Himage))
                print("exit")
                break
            t+=1
            time.sleep(1)
        
    count()
