"""
    This program is for orchestrating everything in Computer Music
    for the Kadenze Office

    map out channel 5-8 to cdromStepperNote
    map out channel 9-12 to HDD stepper control
    map out channel 13-16 to cdromTrey

    The installation will basically act as a clock for the office,
    every two seconds the script performs the following actions

    1.  Check the time, if it is a new hour the installation will play a jingle
    2.  Check the status of the R&D, QA and WebDev Repos, if any new commits
        have been pushed to the masters branch it plays a jingle
    3.  Checks JIRA for the number of active tickets, if the number has decreased
        a jingle will be played. If the number had increased a different jingle
        will be played.
    4.  Checks our user count. If we have gained or lost any of the different
        user types an according jingle will be played.


    --------------- Time Jingles ----------------------------
    Top of the hour : something that has to do with timing, using the hour of
                      the day in the timing signature perhaps

    Noon            : something that utalizes everything, very grand, lots of
                      HDD flopping

    4:00 Silly Hour :

    --------------- Git Jingles -----------------------------

    rnd push:

    web push:

    qa push:

    --------------- JIRA Jingles ----------------------------

    Ticket Created:

    Ticket Closed:

    --------------- User Jingles ----------------------------

    Piano Lost:

    Piano Gained:

    Kazoo Lost:

    Kazoo Gained:

    Cowbell lost:

    Cowbell gained

    --------------------------------------------------------
"""
import time, logging, sys, json, os
import rtmidi
from datetime import datetime
import requests
from kad_users import KadUsers
import git
from git import Repo
from jira import JIRA
import random

"""
log = logging.getLogger('test_midiin_poll')
logging.basicConfig(level=logging.DEBUG)

cdRomArduino = serial.Serial('/dev/cu.usbmodem14211', 57600, timeout = 0.1)
hddStepperArduino = serial.Serial('/dev/cu.usbmodem14221', 57600, timeout = 0.1)
moppyArduino1 = serial.Serial('/dev/cu.usbmodem14231', 57600, timeout = 0.1)
moppyArduino2 = serial.Serial('/dev/cu.usbmodem142411', 57600, timeout = 0.1)
"""

computer_music_port = rtmidi.MidiOut().open_port(0)
moppy_port1 = rtmidi.MidiOut().open_port(1)
moppy_port2 = rtmidi.MidiOut().open_port(2)

available_ports = midiOut.get_ports()

moppy1 = None
moppy2 = None
computer_music = None

for port in available_ports:
    if port == "IAC Driver Moppy Bus 1":
        moppy1 = port
    elif port == 'IAC Driver Moppy Bus 2':
        moppy2 = port
    elif port == 'IAC Driver Computer Music':
        computer_music = port

print('moppy port 1 : ', moppy1)
print('moppy port 2 : ', moppy2)
print('computer music port 2 : ', computer_music)

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


last_commit = ''
last_time = {
        'hour': 12,
        'minute': 12,
        'second': 12
        }

jira_tickets = []
jira_issues = 0

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
    print("playing hourly jingle for the {} hour".format(hour))
    for i in range(hour):
        note_on = [0x90, 50 + i, 112]
        note_off = [0x80,  50 + i, 0]
        midiOut.send_message(note_on)
        time.sleep(0.0125*random.randrange(7))
        midiOut.send_message(note_off)
        time.sleep(0.0125*random.randrange(7))
    for i in range(hour):
        t = hour - i
        note_on = [0x90, 50+t, 112]
        note_off = [0x80,  50+t, 0]
        midiOut.send_message(note_on)
        time.sleep(0.0125*random.randrange(7))
        midiOut.send_message(note_off)
        time.sleep(0.0125*random.randrange(7))

def check_time():
    """
    deals with all of the timing things
    """

    current_time = datetime.now().time()
    global last_time

    # HOURLY DING DING
    if current_time.hour != last_time['hour']:
        last_time['hour'] = current_time.hour
        print("Playing hourly jig : ", last_time)
        # lunchtime song
        hourly_jingle(last_time['hour'])
        if last_time['hour'] == 12:
            print("Its lunch time everyone!!! Lets go to lunch!")
            lunchtime_jingle()

    if current_time.minute!= last_time['minute']:
        last_time['minute'] = current_time.minute

    if current_time.second != last_time['second']:
        last_time['second'] = current_time.second

def _print_time():
    print('[{}:{}:{}]'.format(last_time['hour'], last_time['minute'],
        last_time['second']))

def git_activity():
    """
    if possible, moniter our main repos, or possibly jira and have
    a jingle for each time that changes are pushed to the repo

    """
    # --------------- Web Repo ----------------
    # need access

    # --------------- QA Repo ----------------
    # need access

    # --------------- R&D Repo ----------------
    science_repo = Repo('/Users/nathan/workspace/science').git
    global last_commit
    if last_commit != science_repo.show_branch('master'):
        last_commit = science_repo.show_branch('master')
        print("============ new science commit =================")
        print(last_commit)
        _print_time()
        os.system("say " + last_commit)
        science_updated()

def web_updated():
    pass

def qa_updated():
    pass

def science_updated():
    pass

def jira_activity():
    """
    if possible, moniter jira and have
    a jingle for each time that changes are pushed to the repo

    """

    # --------------- R&D Repo ----------------
    options = {
            'server': 'https://kadenze.atlassian.net'
            }
    server = JIRA(options, basic_auth=('nathan', 'SecurePassword!'))
    # print(server)
    # projects = server.projects()
    # print(projects)
    issues = server.search_issues('')
    global jira_issues
    if len(issues) > jira_issues:
        jira_issues = len(issues)
        message = "new JIRA issue added now at {} issues".format(jira_issues)
        os.system("say " + message)
        # Do a jingle
    elif len(issues) < jira_issues:
        jira_issues = len(issues)
        message = "new JIRA issue resolved now at {} issues".format(jira_issues)
        os.system("say " + message)

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
        _print_time()
        users.cowbell = content['cowbell']
        new_cowbell()
    elif content['cowbell'] < users.cowbell:
        print("---------------------------------")
        print("cowbell count has decreased to {} from {}".format(content['cowbell'],
            users.cowbell))
        _print_time()
        users.cowbell = content['cowbell']
        lost_cowbell()

    # --------- harpsichord ----------
    if content['harpsichord'] > users.harpsichord:
        print("---------------------------------")
        print("harpsichord count has increased to {} from {}".format(content['harpsichord'],
            users.harpsichord))
        _print_time()
        users.harpsichord = content['harpsichord']
        new_harpsichord()
    elif content['harpsichord'] < users.harpsichord:
        print("---------------------------------")
        print("harpsichord count has decreased to {} from {}".format(content['harpsichord'],
            users.harpsichord))
        _print_time()
        users.harpsichord = content['harpsichord']
        lost_harpsichord()

    # --------- ukulele ----------
    if content['ukulele'] > users.ukulele:
        print("---------------------------------")
        print("ukulele count has increased to {} from {}".format(content['ukulele'],
            users.ukulele))
        _print_time()
        users.ukulele = content['ukulele']
        new_ukulele()
    elif content['ukulele'] < users.ukulele:
        print("---------------------------------")
        print("ukulele count has decreased to {} from {}".format(content['ukulele'],
            users.ukulele))
        _print_time()
        users.ukulele = content['ukulele']
        lost_ukulele()

    # --------- piano ----------
    if content['piano'] > users.piano:
        print("---------------------------------")
        print("piano count has increased to {} from {}".format(content['piano'],
            users.piano))
        _print_time()
        users.piano = content['piano']
        new_piano()

    elif content['piano'] < users.piano:
        print("---------------------------------")
        print("piano count has decreased to {} from {}".format(content['piano'],
            users.piano))
        _print_time()
        users.piano = content['piano']
        lost_piano()

    # --------- kazoo ----------
    if content['kazoo'] > users.kazoo:
        print("---------------------------------")
        print("kazoo count has increased to {} from {}".format(content['kazoo'],
            users.kazoo))
        _print_time()
        users.kazoo = content['kazoo']
        new_kazoo()
    elif content['kazoo'] < users.kazoo:
        print("---------------------------------")
        print("kazoo count has decreased to {} from {}".format(content['kazoo'],
            users.kazoo))
        _print_time()
        users.kazoo = content['kazoo']
        lost_kazoo()

    def lunchtime_jig():
        pass

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
        # jira activity
        jira_activity()
        # new users
        new_users()
        time.sleep(2)

if __name__ == '__main__':
    main();
