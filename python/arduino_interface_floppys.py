"""
    This program is for orchestrating everything in Computer Music

    map out channel 5-8 to cdromStepperNote
    map out channel 9-12 to HDD stepper control
    map out channel 13-16 to cdromTrey
"""
import serial, time, random, array, logging, sys
import rtmidi
from rtmidi.midiutil import open_midiport

log = logging.getLogger('test_midiin_poll')
logging.basicConfig(level=logging.DEBUG)

moppyArduino1 = serial.Serial('/dev/cu.usbmodem14231', 57600, timeout = 0.1)
moppyArduino2 = serial.Serial('/dev/cu.usbmodem142411', 57600, timeout = 0.1)

time.sleep(6)

#currentPeriod = [0,0,0,0,0,0,0,0]

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


def moppyNote(driveNum, periodData1, periodData2):
    print("Moppy drive {} was sent period data {}-{}".format(
        driveNum, periodData1, periodData2))
    # firtst byte is the drive number (in multiples of 2)
    # second byte and third byte is what the period is set to
    periodData1 = chr(periodData1)
    periodData2 = chr(periodData2)
    #periodData1 = chr((periodData >> 8) & 0xff)
    #periodDatas = chr((periodData & 0xff))
    if driveNum < 5:
        driveNum = chr(driveNum*2)
        msgString = (driveNum, periodData1, periodData2)
        moppyArduino1.write(msgString)
    elif driveNum < 10:
        driveNum = chr((driveNum-4)*2)
        msgString = (driveNum, periodData1, periodData2)
        moppyArduino2.write(msgString)
    print(msgString)

def main():
    """Main program function"""
    floppyPort = 'IAC Driver Moppy Bus 1'

    try:
        floppyMidiIn, floppyPortName = open_midiport(floppyPort)
    except (EOFError, KeyboardInterrupt):
        sys.exit()
    print("Entering main loop. Press Control-C to exit.")

    try:
        timer = time.time()
        fTimer = time.time()
        while True:
            fmsg = floppyMidiIn.get_message()
            if fmsg:
                message, fDeltatime = fmsg
                fTimer += fDeltatime
                if(type(message) == list and len(message) == 3):
                    try:
                        if message[0] > 127 and message[0] < 144:
                            # note off
                            channel = message[0] - 127
                            moppyNote(channel, 0, 0)

                        if message[0] > 143 and message[0] < 160:
                            # note on
                            channel = message[0] - 143
                            if message[2] == 0:
                                moppyNote(channel, 0, 0)
                                #currentPeriod[channel] = 0
                            else:
                                longPeriod = microPeriods[message[1]] / (ARDUINO_RESOLUTION * 2)
                                print("long period : {}".format(longPeriod))
                                period2 = longPeriod & 0xff
                                period1 = longPeriod >> 8
                                #currentPeriod[channel] = longPeriod
                                moppyNote(channel, period1, period2)

                    except Exception as e:
                        print("error parsing MIDI : {} : {} - {}".format(e, message, type(message)))

            time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        floppyMidiIn.close_port()
        del floppyMidiIn

if __name__ == '__main__':
    main();
