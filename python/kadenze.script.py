"""
    This program is for orchestrating everything in Computer Music
    for the Kadenze Office

    map out channel 5-8 to cdromStepperNote
    map out channel 9-12 to HDD stepper control
    map out channel 13-16 to cdromTrey
"""
import serial, time, random, array, logging, sys
import rtmidi
from rtmidi.midiutil import open_midiport

log = logging.getLogger('test_midiin_poll')
logging.basicConfig(level=logging.DEBUG)

cdRomArduino = serial.Serial('/dev/cu.usbmodem14211', 57600, timeout = 0.1)
hddStepperArduino = serial.Serial('/dev/cu.usbmodem14221', 57600, timeout = 0.1)
moppyArduino1 = serial.Serial('/dev/cu.usbmodem14231', 57600, timeout = 0.1)
moppyArduino2 = serial.Serial('/dev/cu.usbmodem142411', 57600, timeout = 0.1)

midiOut = rtmidi.MidiOut();

time.sleep(6)

ARDUINO_RESOLUTION = 40
microPeriods = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            30578, 28861, 27242, 25713, 24270, 22909, 21622, 20409, 19263, 18182, 17161, 16198, #C1 - B1
            15289, 14436, 13621, 12856, 12135, 11454, 10811, 10205, 9632, 9091, 8581, 8099, #C2 - B2
            7645, 7218, 6811, 6428, 6068, 5727, 5406, 5103, 4816, 4546, 4291, 4050, #C3 - B3
            3823, 3609, 3406, 3214, 3034, 2864, 2703, 2552, 2408, 2273, 2146, 2025, # C4 - B4
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

def main():
    # something to make the midi magic happen

if __name__ == '__main__':
    main();
