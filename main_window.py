# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:29:46 2016

@author: Dominik
"""

import tkinter as tk
import time_manager as tm
from datetime import datetime, timedelta

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.state("zoomed")
        self.configure(bg="black")
        
        self.end_time_file = "end_time.txt"
        
        self.countdown_font_size = 300
        
        
        self.remaining_label = tk.Label(self, text="", width=1,height=1, font=(None,self.countdown_font_size), fg="red", bg="black")        
        self.remaining_label.pack(fill=tk.BOTH, expand=1)
        
        self.blink_on = False
        
        self.bind_keys()
        
        self.remaining = tm.get_remaining_time(self.end_time_file)
        self.countdown()

    def countdown(self):  
        self.remaining = tm.get_remaining_time(self.end_time_file)
        
        if self.remaining.days < 0:
            self.remaining_label.configure(text="0:00:00\nZeit abgelaufen!")
        else:
            self.remaining_label.configure(text=str(timedelta(seconds=self.remaining.seconds)))
            
            #Attention please!
            if (self.remaining.seconds < 10):
                self.toggle_color(self.remaining_label)
            
        self.after(100, self.countdown)
            
    def toggle_color(self, label):
        if self.blink_on:
            label.configure(fg="black", bg="red")
            self.configure(bg="red")
            self.blink_on = False
        else:
            label.configure(fg="red", bg="black")
            self.configure(bg="black")
            self.blink_on = True
            
    def add_seconds(self, event=None):
        tm.add_secs_to_end_time(60)
        
    def sub_seconds(self, event=None):
        tm.add_secs_to_end_time(-60)
    
    def reduce_font_size(self, event=None):
        self.countdown_font_size -= 5
        self.remaining_label.configure(font=(None,self.countdown_font_size))
        
    def increase_font_size(self, event=None):
        self.countdown_font_size += 5
        self.remaining_label.configure(font=(None,self.countdown_font_size))
        
    def bind_keys(self):
        self.bind("+", self.add_seconds)
        self.bind("-", self.sub_seconds)
        self.bind("s", self.reduce_font_size)
        self.bind("w", self.increase_font_size)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()