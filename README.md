# Zooming-Zoomer
Program to automate recording of University Zoom lectures and meetings.

Have you ever been too busy (or too lazy) to attend your university zoom lectures? Well I've been both, and unfortunately for me, the university that I'm at is
very slow at uploading lecture recordings, and it can take up to 48 hours for me to be able to watch them
! Considering I have lecture clashes, or just don't want to get up at 7 in the morning each day, I've made
a utility to record Zoom lectures for me.

### It's like you're there, but you're not.
The way this program works, I'd say it's basically undetectable and indistinguishable from if you were actually watching it live. Since it records the screen
with OBS, and then actually joins Zoom meetings with the
client, it's like you're really there. All you have to do is turn the computer on, start the script up and LEAVE THE COMPUTER ALONE for the duration of your activities.
As this records the screen, you should not use your computer for anything else and close all background programs that might interfere with the recording, or you will get sub-par results.

The process is as follows:

1. Determine what lectures/meetings are on today by a pre-set timetable you entered.
2. Determine what lecture is on next.
3. Wait until the time the lecture starts, then:
4. Launch OBS Studio with the --startrecording flag.
5. Open the Zoom link you set in your timetable.
6. Wait until the lecture/meeting is over, based on the duration you specify in your timetable.
7. Leave the Zoom meeting automatically with keyboard shortcuts.
8. Kill the Zoom and OBS processes
9. Wait until the next lecture and then repeat 3-9, or, if there aren't any left, exit the program.

and badda bing, badda boom, you've got recordings of all your lectures for that day, recorded on your computer and you don't have to wait for your lecturer to upload
them. They also thought you were actually in the meeting if they take attendence based on who's joined the call, since it's an actual Zoom client joining using your account.

### Limitations
As with any software program, there are limitations:
1. This program AT THE MOMENT is LINUX ONLY. I have not made it compatible with other operating systems but will do so in the future.
2. It cannot help if you have timetable clashes that both use Zoom at the same time. Sorry kiddo, unfortunately it's not actually possible for you
to be in two Zoom meetings at once and get the same single-lecture recording functionality in the program's current state. Zoom's ToS prevents you from
joining multiple meetings on multiple computers with the same account, so that won't work either unfortunately.

### Requirements
OBS Studio, Zoom and Python3. In terms of python3 modules, you will need to install pynput and psutil with pip if they are not already installed.
