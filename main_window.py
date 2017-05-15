# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:29:46 2016

@author: Dominik
"""

import tkinter as tk
import tkinter.font
import time_manager as tm
from datetime import datetime, timedelta

import platform


class MainWindow(tk.Tk):
    def __init__(self, window_height, window_width):
        tk.Tk.__init__(self)

        self.title("NightStuff Countdown")
        self.window_width = window_width        
        self.window_height = window_height
        self.geometry("%dx%d" %(self.window_width, self.window_height))

#        self.window_width, self.window_height = self.winfo_screenwidth(), self.winfo_screenheight()
#        self.geometry("%dx%d+0+0" % (self.window_width, self.window_height))
        self.configure(bg="black")
        self.end_time_file = "end_time.txt"
        print(self.winfo_screenwidth(), self.winfo_screenheight())

        self.lift()

        if "windows" in platform.system():
            self.attributes('-topmost', True)
            self.attributes('-topmost', False)
            self.state("zoomed")

        first_row_weight = 0.7
        second_row_weight = 1 - first_row_weight

        # self.grid_rowconfigure(0,minsize=int(first_row_weight*self.window_height))
        self.grid_rowconfigure(2, minsize=int(second_row_weight * self.window_height))
        self.grid_columnconfigure(0, minsize=int(self.window_width))

        font_helv_countdown = tkinter.font.Font(family="Arial", size=int(self.window_height / 2.5))
        font_helv_countdown_name = tkinter.font.Font(family="Arial", size=int(self.window_height * 0.15))

        self.remaining_label = tk.Label(self, text="", width=1, height=1, font=font_helv_countdown, fg="red",
                                        bg="black",anchor="n",pady=-500)
        self.remaining_label.grid(row=0, sticky="wen")

        self.separator = tk.Frame(self, height=3, bg="red")
        self.separator.grid(row=1, sticky="ew")

        self.countdown_to_name_label = tk.Message(self, text="", font=font_helv_countdown_name, fg="red", bg="black",
                                                  width=self.window_width,anchor="n",justify="center")
        self.countdown_to_name_label.grid(row=2)#, sticky="wen")

        self.blink_on = False

        self.bind_keys()

        self.remaining = tm.get_remaining_time(self.end_time_file)
        self.current_hint_text = " "
        self.countdown()

    def countdown(self):
        self.remaining = tm.get_remaining_time(self.end_time_file)
        print("Hello")
        print(self.remaining.seconds)

        new_hint_text = str(tm.get_hint_text_from_txt("hint_text.txt"))

        if not (self.current_hint_text == new_hint_text):
            self.current_hint_text = new_hint_text
            self.countdown_to_name_label.configure(text=self.current_hint_text)

        if self.remaining.days < 0:
            self.remaining_label.configure(text="0:00:00", bg="red", fg="black")
            tm.save_time_to_txt(datetime.now())
        else:
            remaining_time_str = str(timedelta(seconds=self.remaining.seconds))
            self.remaining_label.configure(text=remaining_time_str, bg="black", fg="red")
            tm.save_remaining_time_to_txt(remaining_time_str)

            # Attention please!
        #            if (self.remaining.seconds < 10):
        #                self.toggle_color(self.remaining_label)

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
        self.remaining_label.configure(font=(None, self.countdown_font_size))

    def increase_font_size(self, event=None):
        self.countdown_font_size += 5
        self.remaining_label.configure(font=(None, self.countdown_font_size))

    def bind_keys(self):
        self.bind("+", self.add_seconds)
        self.bind("-", self.sub_seconds)
        self.bind("s", self.reduce_font_size)
        self.bind("w", self.increase_font_size)
        
if __name__ == "__main__":
    window_height = 1080
    winow_width = 1920
    
    countdown_instance = MainWindow(window_height=1080, window_width=1920)
    countdown_instance.mainloop()
