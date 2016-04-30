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

cdRomArduino = serial.Serial('/dev/cu.usbmodem14211', 57600, timeout = 0.1)
hddStepperArduino = serial.Serial('/dev/cu.usbmodem14221', 57600, timeout = 0.1)

midiOut = rtmidi.MidiOut();

time.sleep(6)

def hddStepper(driveNum, velocity):
    """For opening and closing the lid of the HDD's"""
    print("HDD stepper {} triggered at {} velocity".format(driveNum, velocity))
    msg = []
    msg.append(0xff)
    msg.append(driveNum)
    msg.append(velocity)
    hddStepperArduino.write(msg)

def cdRomStepperNote(driveNum, midiNote, velocity):
    """ for sending messages to the stepper motors on CDROMs"""
    flag = chr(255)
    msgType = chr(1)
    driveNum = chr(driveNum)
    midiNote = chr(midiNote)
    velocity = chr(velocity)
    msgString = (flag, msgType, driveNum, midiNote, velocity)
    cdRomArduino.write(msgString)
    print("CDROM stepper {} triggered at midi note {} with velocity {}"\
          .format(driveNum, midiNote, velocity))
    print(msgString)

def cdRomTrey(driveNum):
    """ for pressing the open drive button on the front of the CDROM drive """
    flag = chr(255)
    msgType = chr(1)
    driveNum = chr(driveNum)
    zilch = chr(0)
    msgString = (flag, msgType, driveNum,  zilch, zilch)
    cdRomArduino.write(msgString)
    print("CDROM {}'s trey button had been activated".format(driveNum))


def main():
    """Main program function"""
    port = 'IAC Driver Computer Music'

    try:
        midiin, port_name = open_midiport(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Entering main loop. Press Control-C to exit.")
    try:
        timer = time.time()
        while True:
            msg = midiin.get_message()
            if msg:
                message, deltatime = msg
                timer += deltatime
                if(type(message) == list and len(message) == 3):
                    try:
                        channel = message[0] - 143
                        if (channel > 0):
                            pitch = message[1]
                            velocity = message[2]
                            if channel < 5:
                                #do nothing because this is handled by Moppy
                                print("nothing mapped to these channels")
                            elif channel < 9:
                                cdRomStepperNote(channel-4, pitch, velocity)
                            elif channel < 13:
                                hddStepper(channel - 8, pitch)
                            elif channel < 17:
                                cdRomTrey(channel-12)

                    except Exception as e:
                        print("error parsing MIDI : {} : {} - {}".format(e, message, type(message)))


            time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin

if __name__ == '__main__':
    main();
