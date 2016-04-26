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

# cdRomArduino = serial.Serial('/dev/ttyACM0', 57600, timeout = 0.1)
# stepperArduino = serial.Serial('', 57600, timeout = 0.1)
# hddStepperArduino = serial.Serial('', 57600, timeout = 0.1)

midiOut = rtmidi.MidiOut();

time.sleep(6)

def parseMIDI(channel, pitch, velocity):
    """ Reads a midi message and determines if anything needs to be done"""
    if channel < 5:
        print("nothing mapped to these channels")
        #do nothing because this is handled by Moppy
    elif channel < 9:
        cdRomStepperNote(channel-8, pitch, velocity)
    elif channel < 13:
        hddStepper(channel - 8, pitch, velocity)
    else:
        cdRomTrey(channel-12)

def hddStepper(driveNum, velocity):
    """For opening and closing the lid of the HDD's"""
    msgString = ((driveNum) << 4) + 0x83
    msgString = msgString + (velocity)
    # hddStepperArduino.write(msgString)
    print("HDD stepper {} triggered at {} velocity".format(driveNum, velocity))

def cdRomStepperNote(driveNum, midiNote, velocity):
    """ for sending messages to the stepper motors on CDROMs"""
    msgString = ((driveNum) << 4) + 0x82
    msgString = msgString + (velocity) + (midiNote)
    # cdRomArduino.write(msgString)
    print("CDROM stepper {} triggered at midi note {} with velocity {}"\
          .format(driveNum, midiNote, velocity))

def cdRomTrey(driveNum):
    """ for pressing the open drive button on the front of the CDROM drive """
    msgString = ((driveNum) << 4) + 0x81
    # cdRomArduino.write(cdRomTrey)
    print("CDROM {}'s trey button had been activated".format(driveNum))


def findPort():
    for port in midiOut.get_ports():
        if port == 'IAC Driver Computer Music':
            return port


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))


def main():
    """Main program function"""
    port = findPort();

    try:
        midiin, port_name = open_midiport(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    # print("Attaching MIDI input callback handler.")
    # midiin.set_callback(MidiInputHandler(port_name))

    print("Entering main loop. Press Control-C to exit.")
    try:
        # just wait for keyboard interrupt in main thread
        timer = time.time()
        while True:
            msg = midiin.get_message()
            if msg:
                message, deltatime = msg
                timer += deltatime
                print("[%s] @%0.6f %r" % (port_name, timer, message))
                parseMIDI(message[0], message[1], message[2])

            time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin

if __name__ == '__main__':
    main();

