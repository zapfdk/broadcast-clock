# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:33:21 2016

@author: Dominik
"""


from datetime import datetime, timedelta
import time
import sys
sleep_secs = 0.3

def get_time_from_txt(filename):
    written_yet = False
    while not written_yet:
        try: 
            with open("end_time.txt", "r") as f:
                end_time = f.readline().strip()
                end_time = datetime.strptime(end_time, "%d.%m.%Y.%H:%M:%S")
                return end_time
        except:
            print(sys.exc_info()[0])
            print("Reading from file failed. Trying again in %.1f seconds" %sleep_secs)
            time.sleep(0.3)
    
def save_time_to_txt(end_time):
    written_yet = False
    while not written_yet:
        try:
            with open("end_time.txt", "w") as f:
                f.write(end_time.strftime("%d.%m.%Y.%H:%M:%S"))
            written_yet = True  
        except:
            print(sys.exc_info()[0])
            print("Saving to file failed. Trying again in %.1f seconds" %sleep_secs)
            time.sleep(0.3)
            
def get_hint_text_from_txt(filename):
    written_yet = False
    while not written_yet:
        try: 
            with open(filename, "r") as f:
                hint_text = f.readline().strip()
                return hint_text
        except:
            print(sys.exc_info()[0])
            print("Reading from file failed. Trying again in %.1f seconds" %sleep_secs)
            time.sleep(0.3)
            
def save_hint_text_to_txt(hint_text):
    written_yet = False
    while not written_yet:
        try:
            with open("hint_text.txt", "w") as f:
                f.write(hint_text)
            written_yet = True  
        except:
            print(sys.exc_info()[0])
            print("Saving to file failed. Trying again in %.1f seconds" %sleep_secs)
            time.sleep(0.3)
            
def save_remaining_time_to_txt(remaining_time):
    written_yet = False
    while not written_yet:
        try:
            with open("remaining_time.txt", "w") as f:
                f.write(remaining_time)
            written_yet = True  
        except:
            print(sys.exc_info()[0])
            print("Saving to file failed. Trying again in %.1f seconds" %sleep_secs)
            time.sleep(0.3)
    
def add_secs_to_end_time(delta_seconds):
    current_end_time = get_time_from_txt("end_time.txt")
    new_end_time = current_end_time + timedelta(seconds=delta_seconds)
    save_time_to_txt(new_end_time)
    
def get_remaining_time(filename):
    current_end_time = get_time_from_txt("end_time.txt")
    remaining_time = current_end_time - datetime.now()
    return remaining_time