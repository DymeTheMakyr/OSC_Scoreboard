from tkinter import *
from tkinter import font
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import sys
import threading as th
import argparse

ip = input("IP (A.B.C.D): ")
port = int(input("port (int): "))

covered = True

tScore = 0
sScore = 0

root = Tk()
root.attributes("-fullscreen", True)
root.configure(background="black")

custom_font = font.Font(family="CustomFont", size=80)

Label(root, text="STUDENTS", font=("Arial", 80), background="black", foreground="white").place(anchor="n", relx= 0.25, rely=0.2)
Label(root, text="TEACHERS", font=("Arial", 80), background="black", foreground="white").place(anchor="n", relx=0.75, rely=0.2)

sLabel = Label(root, text=f"{sScore:03}", font=("Arial", 240), background="black", foreground="white")
sLabel.place(anchor="center", relx = 0.25, rely = 0.6)
tLabel = Label(root, text=f"{tScore:03}", font=("Arial", 240), background="black", foreground="white")
tLabel.place(anchor="center", relx = 0.75, rely = 0.6)

Label(root, bg="white").place(relx=0, rely=0, anchor="nw", relwidth=0.01, relheight=1)
Label(root, bg="white").place(relx=0.5, rely=0.5, anchor="center", relwidth=0.01, relheight=1)
Label(root, bg="white").place(relx=1, rely=0, anchor="ne", relwidth=0.01, relheight=1)
Label(root, bg="white").place(relx=0, rely=0, anchor="nw", relwidth=1, relheight=0.02)
Label(root, bg="white").place(relx=0, rely=1, anchor="sw", relwidth=1, relheight=0.02)

cover = Label(root, bg="black")
cover.place(relx=0, rely=0, relwidth=1, relheight=1)

def changeScore(addr, *args):
	global tScore
	global sScore
	global tLabel, sLabel
	print(addr, "\n", args)
	if args[0] == 1:
		tScore += args[1]
		tLabel["text"] = f"{tScore:03}"
	elif args[0] == 0:
		sScore += args[1]
		sLabel["text"] = f"{sScore:03}"
	
def toggleBoard(addr, *args):
	global covered
	if covered:
		cover.place(relx=0,rely=0, anchor="ne", relwidth = 1, relheight=1)
	else:
		cover.place(relx=0,rely=0, anchor="nw", relwidth = 1, relheight=1)
		
	covered = not covered

def mainloop():
	print("Disp Started")
	dispatcher = Dispatcher()
	dispatcher.map("/scoreboard", changeScore)
	dispatcher.map("/scoreboard/toggle", toggleBoard)
	dispatcher.set_default_handler(lambda addr, *args:print(addr, args, "\n", *args))
	server = osc_server.BlockingOSCUDPServer((ip, port), dispatcher)
	server.serve_forever()

mainThread = th.Thread(target=mainloop)
mainThread.daemon = True
mainThread.start()

root.mainloop()
