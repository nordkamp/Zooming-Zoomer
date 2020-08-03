#!/usr/bin/env python
"""Zooming Zoomer v0.1: A script to automatically record university zoom meetings.
Copyright (C) 2020 Matthew Hoffman

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA."""
import sys
from os import system
from time import sleep
from datetime import datetime
from psutil import process_iter
from pynput.keyboard import Key, Controller
__author__ = "Matthew Hoffman"
__copyright__ = "Copyright 2020, Matthew Hoffman"
__version__ = "0.1"
# Here I have provided my timetable as an example.
# Replace and modify it to include yours as you see fit. Make sure
# your time of day is in 24-hour format AND that your 'day' is
# in the same integer format that can be seen in the DAYS dictionary
# (0 for monday, 1 for tuesday, 2 for wednesday, etc.) see how I've put
# it in for clarification.
# FORMAT: activity_name: (day, hour, minute, duration, record?, link)
TIMETABLE = {
    "CSSE2010 LEC1": (0, 8, 0, 1, False, "zoom-link-here"),
    "ENGG1300 LEC1": (0, 8, 0, 2, True, "zoom-link-here"),
    "INFS1200 LEC1": (0, 10, 0, 2, True, "zoom-link-here"),
    "ENGG1200 SMR1": (0, 11, 0, 1, False),
    "CSSE2010 PRA1": (0, 17, 0, 2, True, "zoom-link-here"),
    "INFS1200 TUT1": (1, 10, 0, 1, False),
    "MATH1051 LEC1": (1, 14, 0, 1, True, "zoom-link-here"),
    "ENGG1300 PRA P1": (1, 18, 0, 2, False),
    "MATH1051 LEC2": (2, 11, 0, 1, True, "zoom-link-here"),
    "MATH1051 TUT1": (2, 14, 0, 1, False),
    "ENGG1200 WKS1": (3, 10, 0, 2, False),
    "CSSE2010 LEC2": (3, 13, 0, 1, True, "zoom-link-here"),
    "CSSE2010 PRA2": (3, 14, 0, 2, False),
    "MATH1051 WKS1": (3, 16, 0, 2, False),
    "ENGG1300 PRA P2": (5, 8, 0, 2, False),
    "INFS1200 PRA1": (5, 12, 0, 1, False),
    "MATH1051 LEC3": (5, 13, 0, 1, True, "zoom-link-here")
}
# Dictionary containing a lookup from datetime's day integer to an actual day
DAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

def main():
    """Main function. Handles launching programs, joining meetings and closing
    programs. Also contains the main loop."""
    print("Oh, I'm a zoomy zoomer, yeah!")
    activities_list = get_activities(datetime.now())
    # This loop will run until activities_list is empty.
    while activities_list != []:
        # Get the time right now
        time_obj = datetime.now()
        # Display info about the current time.
        print(f"""------------------------------------------
The current time is: {time_obj.hour}:{time_obj.minute} on {DAYS[time_obj.weekday()]}""")
        # Grab the next activity. Since activities are ordered, we can use pop to get the first
        # item in the activities list, while removing it at the same time.
        next_activity = activities_list.pop(0)
        # Starts OBS and displays the activity to be recorded.
        print(f"Your next recorded activity is: {next_activity[0]} at {next_activity[1][1]}:{next_activity[1][2]}\n{datetime.now()} Starting OBS...")
        start_obs()
        # Once OBS has started, start Zoom and join a meeting.
        print(f"{datetime.now()} OBS Started. Starting Zoom...")
        join_meeting(next_activity[1][5])
        # Waitin' for the meeting to end. Sleep enables this, since it takes an input in seconds, multiply the duration
        # from the timetable dictionary by 3600, as this is 60*60 to convert hours to seconds.
        print(f"{datetime.now()} Meeting theoretically joined.\n{datetime.now()} Waiting for meeting to finish.")
        sleep(next_activity[1][3]*3600)
        print(f"{datetime.now()} Meeting finished. Leaving meeting...")
        sleep(2)
        # Leave the zoom meeting using keyboard shortcuts.
        leave_meeting()
        # Wait for OBS to finish recording the latest relevant info to the file, then kill it.
        print(f"{datetime.now()} Meeting left. Closing OBS...")
        sleep(8)
        close_obs()
        print(f"{datetime.now()} Recording complete.\n------------------------------------------")
    # Exit application once all activities have been recorded.
    print(f"{datetime.now()} No more activities for today!")
    sys.exit()

def leave_meeting():
    """Leave a zoom meeting using the Alt + Q keyboard shortcut."""
    # Initialize controller
    keyboard_1 = Controller()
    # Press zoom "leave meeting" shortcut. If you have this set to
    # anything other than default Alt + Q, please change the code
    # or your custom shortcut back to default
    keyboard_1.press(Key.alt)
    keyboard_1.press("q")
    keyboard_1.release(Key.alt)
    keyboard_1.release("q")
    # Wait for leave meeting button to pop up
    sleep(2)
    # Hit enter on the leave meeting button
    keyboard_1.press(Key.enter)
    keyboard_1.release(Key.enter)
    print("Keystrokes complete")
    # Wait for meeting to be left, then kill zoom.
    sleep(2)
    system("killall -9 zoom")
    print("Zoom closed.")

def join_meeting(link):
    """Join a meeting and wait for it to theoretically connect.
    Parameters:
        link (str): Link to the zoom meeting."""
    # Open link with zoom, as per xdg defaults
    system(f"xdg-open '{link}'")
    sleep(10)

def start_obs():
    """Open OBS in background and start recording automatically."""
    system("screen -m -d obs --startrecording")

def close_obs():
    """Kill OBS after meeting is complete."""
    system("killall -9 obs")

def check_zooming():
    """Check if zoom is currently running."""
    return "zoom" in (process.name() for process in process_iter())

def get_activities(time_obj):
    """Gets a list of today's activities and sorts them according to
    when they occur."""
    possible_activities = {activity:properties for (activity, properties)\
        in TIMETABLE.items() if properties[4] and properties[0] == time_obj.weekday()\
            and time_obj.hour <= properties[1]}
    return sorted(possible_activities.items(), key=lambda x: x[1])

if __name__ == "__main__":
    main()
