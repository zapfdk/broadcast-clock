# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:29:46 2016

@author: Dominik
"""

import tkinter as tk
import time_manager as tm
import time

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.state("zoomed")
        self.label = tk.Label(self, text="", width=10)
        self.label.pack()
        
        print(self.get_remaining_time())       
        
        self.remaining = 0
        self.countdown(10)

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%s" % time.strftime("%H:%M:%S", time.gmtime(self.get_remaining_time())))
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)
            
    def get_remaining_time(self):
        return tm.get_time_from_txt("end_time.txt") - time.localtime()
            

if __name__ == "__main__":
#    tm.save_time_to_txt(time.time()+10)
    app = MainWindow()
    print(app.get_remaining_time())
    app.mainloop()