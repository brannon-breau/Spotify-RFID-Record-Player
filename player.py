#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
import ConfigParser
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="YOUR_DEVICE_ID"
CLIENT_ID="YOUR_CLIENT_ID"
CLIENT_SECRET="YOUR_CLIENT_SECRET"

# Read config file
Config = ConfigParser.ConfigParser()
Config.read("/home/pi/MFRC522-python/RFID-Config.txt")

# From https://wiki.python.org/moin/ConfigParserExamples
def ConfigSectionMap(section):
  dict1 = {}
  options = Config.options(section)
  for option in options:
    try:
        dict1[option] = Config.get(section, option)
        if dict1[option] == -1:
            DebugPrint("skip: %s" % option)
    except:
        print("exception on %s!" % option)
        dict1[option] = None
  return dict1

while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8080",
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
            
            def TagToMplayer (strTag):
                # Read tag attributes from config
                strActionType = ConfigSectionMap(strTag)['actiontype']
                strFileUrlFunction = ConfigSectionMap(strTag)['fileurlfunction']
                
                sp.start_playback(device_id=DEVICE_ID, uris=['spotify:' + strActionType + ':' + strFileUrlFunction])
                sleep(2)
                          
            # DONT include the quotation marks around the card's ID value, just paste the number
            #if (id=='RFID-CARDVALUE-1'):
                
                # playing a song
            #    sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:2vSLxBSZoK0eha4AuhZlXV'])
            #    sleep(2)
                
            #elif (id=='RFID-CARDVALUE-2'):
                
                # playing an album
            #    sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:0JGOiO34nwfUdDrD612dOp')
            #    sleep(2)
                
            # continue adding as many "elifs" for songs/albums that you want to play

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
