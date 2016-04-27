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
hddStepperArduino = serial.Serial('/dev/cu.usbmodem1411', 57600, timeout = 0.1)

midiOut = rtmidi.MidiOut();

time.sleep(6)

def hddStepper(driveNum, velocity):
    """For opening and closing the lid of the HDD's"""
    print("HDD stepper {} triggered at {} velocity".format(driveNum, velocity))
    #msgString = 0xff0148
    msg = []
    #msgString = 0xff
    msg.append(0xff)
    #print(msgString)
    #msgString = (msgString << 8) + driveNum
    msg.append(driveNum)
    #print(msgString)
    #msgString = (msgString << 8) + velocity
    msg.append(velocity)
    #print(msgString)
    hddStepperArduino.write(msg)

def cdRomStepperNote(driveNum, midiNote, velocity):
    """ for sending messages to the stepper motors on CDROMs"""
    msgString = chr(255)
    msgString = msgString + (velocity) + (midiNote)
    # cdRomArduino.write(msgString)
    print("CDROM stepper {} triggered at midi note {} with velocity {}"\
          .format(driveNum, midiNote, velocity))

def cdRomTrey(driveNum):
    """ for pressing the open drive button on the front of the CDROM drive """
    msgString = 0xff
    msgString = (msgString << 8) + driveNum
    msgString = ((driveNum) << 4) + 0x81
    # cdRomArduino.write(cdRomTrey)
    print("CDROM {}'s trey button had been activated".format(driveNum))


def main():
    """Main program function"""
    port = 'IAC Driver Computer Music'

    try:
        midiin, port_name = open_midiport(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    # print("Attaching MIDI input callback handler.")
    # midiin.set_callback(MidiInputHandler(port_name))

    print("Entering main loop. Press Control-C to exit.")
    try:
        timer = time.time()
        while True:
            msg = midiin.get_message()
            if msg:
                message, deltatime = msg
                #print("m1 : ", message[0], " m2 : ", message[1], " m3 : ", message[2])
                timer += deltatime
                # print("%r" % (message))
                if(type(message) == list and len(message) == 3):
                    try:
                        channel = message[0] - 143
                        if (channel > 0):
                            pitch = message[1]
                            velocity = message[2]
                            #print("channel is {}".format(channel))
                            if channel < 5:
                                "string"
                                #print("nothing mapped to these channels")
                                #do nothing because this is handled by Moppy
                            elif channel < 9:
                                "string"
                                #print("cd stepper note will go here")
                                # cdRomStepperNote(channel-8, pitch, velocity)
                            elif channel < 13:
                                "string"
                                hddStepper(channel - 8, pitch)
                                #print("HDD STEPPER HEPPENED")
                            elif channel < 17:
                                "string"
                                # cdRomTrey(channel-12)
                                #print("cdRomTrey willl be going here")
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

