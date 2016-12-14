# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:18:18 2016

@author: dominik
"""

import sys
import os

import main_window
import time_manager as tm


def start_countdown_instance():
    countdown_instance = main_window.MainWindow()
    countdown_instance.mainloop()


def check_arguments(arguments):
    if arguments[1] == "-start":
        pid = str(os.getpid())
        pidfile = "broadcast_countdown.pid"

        if os.path.isfile(pidfile):
            print("%s process is already running." % pidfile)
            sys.exit()

        try:
            with open(pidfile, "w") as f:
                f.write(pid)
            start_countdown_instance()
        finally:
            if os.path.exists("broadcast_countdown.pid"):
                os.remove("broadcast_countdown.pid")

    if "-a" in arguments or "-s" in arguments:
        delta_seconds = 0

        if sys.argv[1] == "-a":
            delta_seconds = int(sys.argv[2])
        elif sys.argv[1] == "-s":
            delta_seconds = -int(sys.argv[2])

        tm.add_secs_to_end_time(delta_seconds)


if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) <= 1:
        print("Please use command line arguments to do something:")
        print("\tUse -start to begin the countdown")
        print("\tUse -a <seconds> or -s <seconds> to add or subtract seconds to the countdown\n")
        sys.exit()
    else:
        check_arguments(arguments)
