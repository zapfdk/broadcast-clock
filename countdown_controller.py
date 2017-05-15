# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 20:18:49 2016

@author: Dominik
"""

import tkinter as tk
from functools import partial
import socket
from datetime import datetime, timedelta
import traceback

EXPAND_GRID_CELL = tk.N + tk.E + tk.W + tk.S


class CountdownController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Countdown Controller")

        self.default_bg = self.cget("bg")

        self.countdown_str_format = "%H:%M:%S"
        self.standard_datetime_format = "%Y-%m-%d %H:%M:%S"

        self.ip_label = tk.Label(self, text="IP: ")
        self.ip_label.grid(row=0, column=0, stick=tk.E)

        self.ip_entry_var = tk.StringVar(self, value="141.24.42.20")
        self.ip_entry = tk.Entry(self, textvariable=self.ip_entry_var)
        self.ip_entry.grid(row=0, column=1)

        self.port_label = tk.Label(self, text="Port: ")
        self.port_label.grid(row=0, column=2, stick=tk.E)

        self.port_entry_var = tk.StringVar(self, value="5005")
        self.port_entry = tk.Entry(self, textvariable=self.port_entry_var)
        self.port_entry.grid(row=0, column=3)

        self.tcp_ip = self.ip_entry_var.get()
        self.tcp_port = int(self.port_entry_var.get())
        self.buffer_size = 1024

        self.connection_checked = False

        self.connect_button = tk.Button(self, text="Check Connection", command=self.on_press_connect, bg="red")
        self.connect_button.grid(row=0, column=4)

        new_button = self.return_new_button("+10 Min.", 600)
        new_button.grid(row=4, column=2)
        new_button = self.return_new_button("-10 Min.", -600)
        new_button.grid(row=5, column=2)
        new_button = self.return_new_button("+1 Min.", 60)
        new_button.grid(row=4, column=3)
        new_button = self.return_new_button("-1 Min.", 60)
        new_button.grid(row=5, column=3)
        new_button = self.return_new_button("+10 Sek.", 10)
        new_button.grid(row=4, column=4)
        new_button = self.return_new_button("-10 Sek.", -10)
        new_button.grid(row=5, column=4)
        new_button = self.return_new_button("+1 Sek.", 1)
        new_button.grid(row=4, column=5)
        new_button = self.return_new_button("-1 Sek.", -1)
        new_button.grid(row=5, column=5)

        self.hint_text_entry_var = tk.StringVar(self, value="Hint Text")
        self.hint_text_entry = tk.Entry(self, textvariable=self.hint_text_entry_var)
        self.hint_text_entry.grid(row=3, column=1, rowspan=1, columnspan=3, sticky=EXPAND_GRID_CELL)
        self.hint_text_entry.bind("<Return>", self.on_press_return)

        self.hint_text_button = tk.Button(self, text="Sende Text", command=self.on_press_send_text)
        self.hint_text_button.grid(row=3, column=4, sticky=EXPAND_GRID_CELL)

        self.countdown_label = tk.Label(self, text="Verbleibende Zeit: ")
        self.countdown_label.grid(row=4, column=0, sticky="e")
        self.remaining_time_label = tk.Label(self, text="0:00:00")
        self.remaining_time_label.grid(row=4, column=1, sticky="w")

        self.countdown_end_label = tk.Label(self, text="Aktuelle Countdownendzeit: ")
        self.countdown_end_label.grid(row=5, column=0, sticky="e")
        self.countdown_end_var_label = tk.Label(self, text="0:00:00")
        self.countdown_end_var_label.grid(row=5, column=1, sticky="w")

        self.hint_label = tk.Message(self, text="Aktueller Hinweistext: ")
        self.hint_label.grid(row=6, column=0, sticky="e")
        self.current_hint_label = tk.Label(self, text=self.hint_text_entry_var.get())
        self.current_hint_label.grid(row=6, column=1, sticky="w")

        self.add_set_countdown()
        self.add_set_end_time()

        self.live_countdown_loop()

    def return_new_button(self, button_text, button_seconds):
        return tk.Button(self, text=button_text, command=partial(self.on_press_add_seconds, button_seconds), width=10)

    def on_press_return(self, event=None):
        focused_widget = self.focus_get()

        if focused_widget == self.hint_text_entry:
            self.on_press_send_text()
        elif focused_widget == self.countdown_entry:
            self.on_press_send_set_countdown()
        elif focused_widget == self.end_time_entry:
            self.on_press_send_end_time()

        self.focus()

    def add_set_countdown(self):
        self.set_countdown = tk.Label(self, text="Setze Countdown: ")
        self.set_countdown.grid(row=7, column=0, sticky="e")

        self.countdown_entry_var = tk.StringVar(self, value="0:00:00")
        self.countdown_entry = tk.Entry(self, textvariable=self.countdown_entry_var, width=5)
        self.countdown_entry.grid(row=7, column=1, rowspan=1, sticky=EXPAND_GRID_CELL)
        self.countdown_entry.bind("<Return>", self.on_press_return)

        self.set_countdown_button = tk.Button(self, text="Senden", command=self.on_press_send_set_countdown)
        self.set_countdown_button.grid(row=7, column=2, sticky=EXPAND_GRID_CELL)

        self.set_countdown_err = tk.Label(self, text="", fg="red")
        self.set_countdown_err.grid(row=7, column=3)

    def add_set_end_time(self):
        self.set_end_time = tk.Label(self, text="Setze Endzeit: ")
        self.set_end_time.grid(row=8, column=0, sticky="e")

        self.end_time_entry_var = tk.StringVar(self, value="0:00:00")
        self.end_time_entry = tk.Entry(self, textvariable=self.end_time_entry_var, width=5)
        self.end_time_entry.grid(row=8, column=1, rowspan=1, sticky=EXPAND_GRID_CELL)
        self.end_time_entry.bind("<Return>", self.on_press_return)

        self.set_end_time_button = tk.Button(self, text="Senden", command=self.on_press_send_end_time)
        self.set_end_time_button.grid(row=8, column=2, sticky=EXPAND_GRID_CELL)

        self.set_end_time_err = tk.Label(self, text="", fg="red")
        self.set_end_time_err.grid(row=8, column=3)

    def live_countdown_loop(self):
        if self.connection_checked:
            remaining_time = ""
            current_hint = ""

            print("yesyesyes")

            self.create_socket()
            self.s.send("-getremainingtime".encode())
            remaining_time = self.get_recv_str()
            self.remaining_time_label.configure(text=remaining_time)
            self.s.close()

            self.create_socket()
            self.s.send("-gethinttext".encode())
            current_hint = self.get_recv_str()
            self.current_hint_label.configure(text=current_hint)
            self.s.close()

            self.create_socket()
            self.s.send("-getendtime".encode())
            end_time = self.get_recv_str()
            end_date_time = datetime.strptime(end_time, self.standard_datetime_format)
            self.countdown_end_var_label.configure(text=end_date_time.strftime("%H:%M:%S"))
            self.s.close()

            countdown = self.countdown_entry_var.get()
            try:
                datetime.strptime(countdown, self.countdown_str_format)
                self.countdown_entry.configure(bg="white")
                self.set_countdown_err.configure(text="")
            except:
                self.countdown_entry.configure(bg="red")
                self.set_countdown_err.configure(text="Fehler mit dem Format. Zeit muss so formatiert sein: HH:MM:SS")

            end_time = self.end_time_entry_var.get()
            try:
                datetime.strptime(end_time, self.countdown_str_format)
                self.end_time_entry.configure(bg="white")
                self.set_end_time_err.configure(text="")
            except:
                self.end_time_entry.configure(bg="red")
                self.set_end_time_err.configure(text="Fehler mit dem Format. Zeit muss so formatiert sein: HH:MM:SS")

        else:
            print("Check connection first...")

        self.after(5000, self.live_countdown_loop)

    def on_press_connect(self):
        try:
            self.tcp_ip = self.ip_entry_var.get()
            self.tcp_port = int(self.port_entry_var.get())
            self.create_socket()
            self.s.send("-check".encode())
            answer = self.s.recv(self.buffer_size)
            answer = answer.decode()

            if answer == "check":
                self.connect_button.configure(bg="green", text="Connected")
                print("Connected with: ", self.tcp_ip, self.tcp_port)
                self.connection_checked = True
            else:
                self.connect_button.configure(bg="red", text="Not Connected")
                self.connection_checked = False

            self.s.close()

            self.focus()
        except:
            self.connect_button.configure(bg="red", text="Not Connected")
            self.connection_checked = False
            print("Something wrong with IP or Port: ")
            traceback.print_exc()


    def on_press_send_set_countdown(self, event=None):
        countdown = self.countdown_entry_var.get()
        try:
            countdown_time = datetime.strptime(countdown, self.countdown_str_format)
            countdown_delta = timedelta(hours=countdown_time.hour, minutes=countdown_time.minute,
                                        seconds=countdown_time.second)

            current_time = datetime.strptime(self.remaining_time_label["text"], self.countdown_str_format)
            current_delta = timedelta(hours=current_time.hour, minutes=current_time.minute,
                                      seconds=current_time.second)

            time_delta = abs(countdown_delta - current_delta)

            if countdown_delta > current_delta:
                self.on_press_add_seconds(time_delta.seconds)
            else:
                self.on_press_add_seconds(-time_delta.seconds)

            self.set_countdown_button.configure(bg="green")

            self.focus()
        except:
            self.set_countdown_button.configure(bg="red")

    def on_press_send_end_time(self, event=None):
        end_time = self.end_time_entry_var.get()
        try:
            current_time = datetime.now()
            current_time_delta = timedelta(hours=current_time.hour, minutes=current_time.minute,
                                           seconds=current_time.second)

            end_date_time = datetime.strptime(end_time, self.countdown_str_format)
            end_time_delta = timedelta(hours=end_date_time.hour, minutes=end_date_time.minute,
                                       seconds=end_date_time.second)

            current_time = datetime.strptime(self.remaining_time_label["text"], self.countdown_str_format)
            current_delta = timedelta(hours=current_time.hour, minutes=current_time.minute,
                                      seconds=current_time.second)

            if end_time_delta > current_time_delta:
                time_delta = end_time_delta - current_time_delta

                #Subtract one second to account for calculation time. Ugly as hell
                if time_delta.seconds > current_delta.seconds:
                    self.on_press_add_seconds(time_delta.seconds - current_delta.seconds - 1)
                else:
                    self.on_press_add_seconds(time_delta.seconds - current_delta.seconds - 1)

                self.set_end_time_button.configure(bg="green", text="Erfolg.")
            else:
                self.set_end_time_button.configure(bg="red", text="Endzeit muss in der Zukunft liegen.")

            self.focus()
        except:
            self.set_end_time_button.configure(bg="red")

    def on_press_send_text(self, event=None):
        hint_text = self.hint_text_entry_var.get()

        try:
            self.create_socket()

            command = "-settext " + hint_text
            self.s.send(command.encode())
            answer = self.get_recv_str()
            self.s.close()

            if answer == "check":
                self.hint_text_button.configure(bg="green")
                self.focus()
            else:
                self.hint_text_button.configure(bg="red")
        except:
            self.hint_text_button.configure(bg="red")

    def on_press_add_seconds(self, delta_seconds):
        self.create_socket()

        command = ""
        if delta_seconds >= 0:
            command = "-a " + str(delta_seconds)
        else:
            command = "-s " + str(delta_seconds * -1)
        self.s.send(command.encode())

        answer = self.s.recv(self.buffer_size)
        print(answer.decode())

        self.s.close()

    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.tcp_ip, self.tcp_port))

    def get_recv_str(self):
        return self.s.recv(self.buffer_size).decode()


if __name__ == "__main__":
    countdown_controller = CountdownController()
    countdown_controller.mainloop()
