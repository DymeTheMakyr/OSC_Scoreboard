from tkinter import *
from tkinter import font
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import sys
import threading as th
import argparse

ip = input("IP (A.B.C.D): ")
port = int(input("port (int): "))



tScore = 0
sScore = 0

root = Tk()
root.attributes("-fullscreen", True)
root.configure(background="black")

custom_font = font.Font(family="CustomFont", size=80)

Label(root, text="STUDENTS", font=("Arial", 80), background="black", foreground="white").place(anchor="n", relx= 0.25, rely=0.1)
Label(root, text="TEACHERS", font=("Arial", 80), background="black", foreground="white").place(anchor="n", relx=0.75, rely=0.1)

sLabel = Label(root, text=sScore, font=("Arial", 240), background="black", foreground="white")
sLabel.place(anchor="center", relx = 0.25, rely = 0.5)
tLabel = Label(root, text=tScore, font=("Arial", 240), background="black", foreground="white")
tLabel.place(anchor="center", relx = 0.75, rely = 0.5)

def changeScore(cont, value):
	print(cont, "\n", value)
	if cont == 1:
		temp = int(tScore.get())
		temp += value
		tScore.set("{temp:03}")
	elif cont == 0:
		temp = int(sScore.get())
		temp += value
		tScore.set("{temp:03}")
		
	
def mainloop():
	print("Disp Started")
	dispatcher = Dispatcher()
	dispatcher.map("/scoreboard", changeScore)
	dispatcher.set_default_handler(print)
	server = osc_server.BlockingOSCUDPServer((ip, port), dispatcher)
	server.serve_forever()

mainThread = th.Thread(target=mainloop)
mainThread.start()

root.mainloop()
