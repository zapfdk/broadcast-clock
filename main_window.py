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
        
        self.remaining_label = tk.Label(self, text="", width=10)
#        sel
        self.remaining_label.grid(row=0)
        
        self.remaining = tm.get_remaining_time(self.end_time_file)
        self.countdown()

    def countdown(self):       
        if self.remaining.days < 0:
            self.remaining_label.configure(text="time's up!")
        else:
            self.remaining = tm.get_remaining_time(self.end_time_file)
            self.remaining_label.configure(text=str(timedelta(seconds=self.remaining.seconds)))
            self.after(1000, self.countdown)            

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()