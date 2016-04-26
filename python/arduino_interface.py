"""

    This program is for orchestrating everything in Computer Music

"""
import serial, time, random, array
import OSC, threading

# connect to computers virtual MIDI bus

# map out channel 1-4 to cdromTrey
# map out channel 5-8 to cdromStepperNote

cdRomArduino = serial.Serial('/dev/ttyACM0', 57600, timeout = 0.1)
stepperArduino = serial.Serial('', 57600, timeout = 0.1)

time.sleep(6)

def parseMIDI(channel, pitch, velocity):
    """ Reads a midi message and determines if anything needs to be done"""
    if channel > 8 and channel < 13:
        cdRomStepperNote(channel-8, pitch, velocity*20)
    else if channel > 12:
        cdRomTrey(channel-12)

def floppyStepperNote(driveNum, midiNote, duration):
    #send this shit

def cdRomStepperStop(driveNum):
    # send this shit

def cdRomStepperNote(driveNum, midiNote, direction):
    msg = driverNum
    # send this shit

def cdRomTrey(driveNum):
    # send this shit

