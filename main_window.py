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
        
        self.end_time_file = "end_time.txt"
        
        self.remaining_label = tk.Label(self, text="", width=10, font=(None,300), fg="red")        
        self.remaining_label.pack()
        
        self.blink_on = False
        
        
        self.remaining = tm.get_remaining_time(self.end_time_file)
        self.countdown()

    def countdown(self):       
        if self.remaining.days < 0:
            self.remaining_label.configure(text="Zeit abgelaufen!")
        else:
            self.remaining = tm.get_remaining_time(self.end_time_file)
            self.remaining_label.configure(text=str(timedelta(seconds=self.remaining.seconds)))
            
            #Attention please!
            if (self.remaining.seconds < 10):
                self.toggle_color(self.remaining_label)
            
            self.after(1000, self.countdown)
            
    def toggle_color(self, label):
        if self.blink_on:
            label.configure(fg="white", bg="red")
            self.blink_on = False
        else:
            label.configure(fg="red", bg="white")
            self.blink_on = True

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()