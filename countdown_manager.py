# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:18:18 2016

@author: dominik
"""

import sys

import main_window
import time_manager as tm

def start_countdown_instance():
    countdown_instance = main_window.MainWindow()
    countdown_instance.mainloop()

if __name__ == "__main__":
    arguments = sys.argv
    
    if sys.argv[1] == "start":
        start_countdown_instance()
    
    if "-a"in arguments or "-s" in arguments:
        delta_seconds = 0
            
        if sys.argv[1] == "-a":
            delta_seconds = int(sys.argv[2])
        elif sys.argv[1] == "-s":
            delta_seconds = -int(sys.argv[2])
        
        tm.add_secs_to_end_time(delta_seconds)
        
        
    
    
    