# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:33:21 2016

@author: Dominik
"""

import time
import sys

def get_time_from_txt(filename):
    try: 
        with open("end_time.txt", "r") as f:
            end_time = f.readline().strip()
            print(end_time)
            end_time = time.strptime(end_time, "%d.%m.%Y.%H:%M:%S")
            return end_time
    except:
        print(sys.exc_info()[0])
        return 0
        
    
def save_time_to_txt(end_time):
    written_yet = False
    while not written_yet:
        try:
            with open("end_time.txt", "w") as f:
                f.write(time.strftime("%d.%m.%Y.%H:%M:%S", end_time))
            written_yet = True  
        except:
            print(sys.exc_info()[0])
            time.sleep(0.3)
        
    
def add_secs_to_end_time(seconds):
    current_end_time = get_time_from_txt("end_time.txt")
    
    
current_end_time = get_time_from_txt("end_time.txt")
print(current_end_time)

current_end_time.tm_sec += 10

print(current_end_time)

    

            