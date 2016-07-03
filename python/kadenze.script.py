"""
    This program is for orchestrating everything in Computer Music
    for the Kadenze Office

    map out channel 5-8 to cdromStepperNote
    map out channel 9-12 to HDD stepper control
    map out channel 13-16 to cdromTrey
"""
import serial, time, logging, sys, json
import rtmidi
from rtmidi.midiutil import open_midiport
from datetime import datetime
import requests
from kad_users import KadUsers

"""
log = logging.getLogger('test_midiin_poll')
logging.basicConfig(level=logging.DEBUG)

cdRomArduino = serial.Serial('/dev/cu.usbmodem14211', 57600, timeout = 0.1)
hddStepperArduino = serial.Serial('/dev/cu.usbmodem14221', 57600, timeout = 0.1)
moppyArduino1 = serial.Serial('/dev/cu.usbmodem14231', 57600, timeout = 0.1)
moppyArduino2 = serial.Serial('/dev/cu.usbmodem142411', 57600, timeout = 0.1)

midiOut = rtmidi.MidiOut();

time.sleep(6)

ARDUINO_RESOLUTION = 40
microPeriods = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                30578, 28861, 27242, 25713, 24270,
                22909, 21622, 20409, 19263, 18182,
                17161, 16198, #C1 - B1
                15289, 14436, 13621, 12856, 12135,
                11454, 10811, 10205, 9632, 9091,
                8581, 8099, #C2 - B2
                7645, 7218, 6811, 6428, 6068, 5727,
                5406, 5103, 4816, 4546, 4291, 4050, #C3 - B3
                3823, 3609, 3406, 3214, 3034, 2864,
                2703, 2552, 2408, 2273, 2146, 2025, # C4 - B4
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

"""

last_time = {
        'hour': 12,
        'minute': 12,
        'second': 12
        }

users = KadUsers()


def lunchtime_jingle():
    """
    This is the song/jingle that will play at noon in the office
    """
    pass

def hourly_jingle(hour):
    """
    This is the song/jingle that will play on the hour in the office

    The timing should vary depending on the time of the day

    Also perhaps
    """

def check_time():
    """
    deals with all of the timing things
    """

    current_time = datetime.now().time()
    global last_time

    # HOURLY DING DING
    if current_time.hour != last_time['hour']:
        last_time['hour'] = current_time.hour
        # lunchtime song
        if last_time['hour'] == 12:
            pass

    if current_time.minute!= last_time['minute']:
        last_time['minute'] = current_time.minute

    if current_time.second != last_time['second']:
        last_time['second'] = current_time.second

def git_activity():
    """
    if possible, moniter our main repos, or possibly jira and have
    a jingle for each time that changes are pushed to the repo

    """
    pass

def new_users():
    """
    Function that monitors new kadenze users and has a jingle for each new
    uke, cowbell and xxx

    """
    global users
    content = json.loads(
            requests.get(
            'https://www.kadenze.com/admin/7d944013-afeb-40c9-94ad-11bbc41bef9e.json').\
            content.decode('utf-8'))

    # --------- cowbell ----------
    if content['cowbell'] > users.cowbell:
        print("---------------------------------")
        print("cowbell count has increased to {} from {}".format(content['cowbell'],
            users.cowbell))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.cowbell = content['cowbell']
        new_cowbell()
    elif content['cowbell'] < users.cowbell:
        print("---------------------------------")
        print("cowbell count has decreased to {} from {}".format(content['cowbell'],
            users.cowbell))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.cowbell = content['cowbell']
        lost_cowbell()

    # --------- harpsichord ----------
    if content['harpsichord'] > users.harpsichord:
        print("---------------------------------")
        print("harpsichord count has increased to {} from {}".format(content['harpsichord'],
            users.harpsichord))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.harpsichord = content['harpsichord']
        new_harpsichord()
    elif content['harpsichord'] < users.harpsichord:
        print("---------------------------------")
        print("harpsichord count has decreased to {} from {}".format(content['harpsichord'],
            users.harpsichord))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.harpsichord = content['harpsichord']
        lost_harpsichord()

    # --------- ukulele ----------
    if content['ukulele'] > users.ukulele:
        print("---------------------------------")
        print("ukulele count has increased to {} from {}".format(content['ukulele'],
            users.ukulele))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.ukulele = content['ukulele']
        new_ukulele()
    elif content['ukulele'] < users.ukulele:
        print("---------------------------------")
        print("ukulele count has decreased to {} from {}".format(content['ukulele'],
            users.ukulele))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.ukulele = content['ukulele']
        lost_ukulele()

    # --------- piano ----------
    if content['piano'] > users.piano:
        print("---------------------------------")
        print("piano count has increased to {} from {}".format(content['piano'],
            users.piano))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.piano = content['piano']
        new_piano()

    elif content['piano'] < users.piano:
        print("---------------------------------")
        print("piano count has decreased to {} from {}".format(content['piano'],
            users.piano))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.piano = content['piano']
        lost_piano()

    # --------- kazoo ----------
    if content['kazoo'] > users.kazoo:
        print("---------------------------------")
        print("kazoo count has decreased to {} from {}".format(content['kazoo'],
            users.kazoo))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.kazoo = content['kazoo']
        new_kazoo()
    elif content['kazoo'] < users.kazoo:
        print("---------------------------------")
        print("kazoo count has increased to {} from {}".format(content['kazoo'],
            users.kazoo))
        print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
            last_time['second']))
        users.kazoo = content['kazoo']
        lost_kazoo()

def new_kazoo():
    pass

def lost_kazoo():
    pass

def new_piano():
    pass

def lost_piano():
    pass

def new_ukulele():
    pass

def lost_ukulele():
    pass

def new_harpsichord():
    pass

def lost_harpsichord():
    pass

def new_cowbell():
    pass

def lost_cowbell():
    pass

def main():
    # something to make the midi magic happen
    while True:
        # clock aspects
        check_time()
        # git activity
        git_activity()
        # new users
        new_users()
        time.sleep(2)

if __name__ == '__main__':
    main();
