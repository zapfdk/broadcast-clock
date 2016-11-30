# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 20:18:49 2016

@author: Dominik
"""

import tkinter as tk
from functools import partial
import socket

import time_manager as tm

expand_grid_cell = tk.N+tk.E+tk.W+tk.S

class CountdownController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Countdown Controller")
        
        self.default_bg = self.cget("bg")
        
        self.ip_label = tk.Label(self,text="IP: ")
        self.ip_label.grid(row=0,column=0,stick=tk.E)
        
        self.ip_entry_var = tk.StringVar(self,value="141.24.42.20")
        self.ip_entry = tk.Entry(self,textvariable=self.ip_entry_var)
        self.ip_entry.grid(row=0,column=1)
        
        self.port_label = tk.Label(self,text="Port: ")
        self.port_label.grid(row=0,column=2,stick=tk.E)
        
        self.port_entry_var = tk.StringVar(self,value="5005")
        self.port_entry = tk.Entry(self,textvariable=self.port_entry_var)
        self.port_entry.grid(row=0,column=3)
        
        self.tcp_ip = self.ip_entry_var.get()
        self.tcp_port = int(self.port_entry_var.get())
        self.buffer_size = 1024
        
        self.connection_checked = False
        
        self.connect_button = tk.Button(self, text="Check Connection",command=self.on_press_connect,bg="red")
        self.connect_button.grid(row=0,column=4)
        
        self.add_minute_button = tk.Button(self, text="+1 Min.",command=partial(self.on_press_add_seconds,60))
        self.add_minute_button.grid(row=1,column=1,sticky=expand_grid_cell)
        
        self.sub_minute_button = tk.Button(self, text="-1 Min.",command=partial(self.on_press_add_seconds,-60))
        self.sub_minute_button.grid(row=2,column=1,sticky=expand_grid_cell)
        
        self.add_half_minute_button = tk.Button(self, text="+30 Sek.",command=partial(self.on_press_add_seconds,30))
        self.add_half_minute_button.grid(row=1,column=3,sticky=expand_grid_cell)
        
        self.sub_half_minute_button = tk.Button(self, text="-30 Sek.",command=partial(self.on_press_add_seconds,-30))
        self.sub_half_minute_button.grid(row=2,column=3,sticky=expand_grid_cell)
        
        self.hint_text_entry_var = tk.StringVar(self,value="Hint Text")
        self.hint_text_entry = tk.Entry(self,textvariable=self.hint_text_entry_var)
        self.hint_text_entry.grid(row=3,column=1,rowspan=1,columnspan=3,sticky=expand_grid_cell)
        self.hint_text_entry.bind("<Return>", self.on_press_send_text)
        
        self.hint_text_button = tk.Button(self, text="Send Text (max. 15 Zeichen)",command=self.on_press_send_text)
        self.hint_text_button.grid(row=3,column=4,sticky=expand_grid_cell)
        
        
        self.countdown_label = tk.Label(self, text="Verbleibende Zeit: ")
        self.countdown_label.grid(row=4,column=0,sticky="e")        
        self.remaining_time_label = tk.Label(self, text="0:00:00")
        self.remaining_time_label.grid(row=4,column=1,sticky="w")    
        
        self.countdown_end_label = tk.Label(self, text="Aktuelle Countdownendzeit: ")
        self.countdown_end_label.grid(row=5,column=0, sticky="e")
        self.countdown_end_var_label = tk.Label(self, text="0:00:00")
        self.countdown_end_var_label.grid(row=5,column=1,sticky="w")
        
        self.hint_label = tk.Label(self, text="Aktueller Hinweistext: ")
        self.hint_label.grid(row=6,column=0,sticky="e")
        self.current_hint_label = tk.Label(self, text=self.hint_text_entry_var.get())
        self.current_hint_label.grid(row=6,column=1,sticky="w")
        
        self.live_countdown_loop()
        
    def live_countdown_loop(self):
        if self.connection_checked:
            remaining_time = ""
            current_hint = ""
            
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
            current_hint = self.get_recv_str()
            self.countdown_end_var_label.configure(text=current_hint)
            self.s.close()
            
            if len(self.hint_text_entry_var.get()) > 15:
                self.hint_text_entry.configure(bg="red")
            else: 
                self.hint_text_entry.configure(bg="white")
        else:
            print("Check connection first...")
        
        self.after(100, self.live_countdown_loop)
        
    def on_press_connect(self):
        self.tcp_ip = self.ip_entry_var.get()
        self.tcp_port = int(self.port_entry_var.get())
        self.create_socket()
        self.s.send("-check".encode())
        answer = self.s.recv(self.buffer_size)
        answer = answer.decode()
        
        if answer == "check":            
            self.connect_button.configure(bg="green",text="Connected")
            print("Connected with: ", self.tcp_ip, self.tcp_port)
            self.connection_checked = True
        
        self.s.close()    
        
        self.focus()
        
    def on_press_send_text(self, event=None):
        hint_text = self.hint_text_entry_var.get()
        
        self.create_socket()
        
        if len(hint_text) <= 15:
            command = "-settext " + hint_text
            self.s.send(command.encode())
            self.focus()
            answer = self.get_recv_str()
            print(answer)
            self.hint_text_button.configure(bg=self.default_bg)
            
            self.s.close()
        else:
            self.hint_text_button.configure(bg="red")
        
    def on_press_add_seconds(self, delta_seconds):
        self.create_socket()
        
        command = ""
        if delta_seconds >= 0:
            command = "-a " + str(delta_seconds)
        else:
            command = "-s " + str(delta_seconds*-1) 
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
        