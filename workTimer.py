# Tcl/tk

import tkinter as tk
import datetime
import threading
import time
import random

shortBreak = 60* 10
shortBreakDuration = 20
longBreak = 60* 60
longBreakDuration = 60* 1

def getBreakAndTime():
    now = datetime.datetime.now()
    today = now.date()
    today = datetime.datetime(today.year, today.month, today.day)

    ssmn = (now-today).seconds # seconds since mid night
    seconds4shortBreak = shortBreak - (ssmn%shortBreak)
    seconds4longBreak = longBreak - (ssmn%longBreak)
    
    if seconds4shortBreak == seconds4longBreak:
        typeOfBreak = 'long'
        interval = seconds4longBreak
    else:
        typeOfBreak = 'short'
        interval = seconds4shortBreak
        
    return interval, typeOfBreak
def hide():
    root.withdraw()
def show():
    root.deiconify()
    root.lift()
def clock(typeOfBreak):
    updateText(typeOfBreak)
    
    show()
    if typeOfBreak == 'short':
        root.after(shortBreakDuration*1000, hide)
    else:
        root.after(longBreakDuration*1000, hide)
    
    interval, typeOfBreak = getBreakAndTime()
    root.after(interval*1000, clock, typeOfBreak) # run itself again after 1000 ms
def updateText(typeOfBreak):
    now = datetime.datetime.now()
    now = now.time()
    now = now.isoformat()[:8]
    quote = quotes[random.randint(0,nquotes)]
    dataobj = [typeOfBreak, now, quote[0], quote[1]]
    for i in range(len(W)):
        W[i].config(text=dataobj[i])
def readQuotes():
    with open('quotes.txt') as f:
        text = f.readlines()

    nquotes = len(text)
    quotes = []
    for i in range(nquotes):
        temp = text[i].replace('\n','').split('-')

        if len(temp) == 2:
            quote = temp[0]
            source = temp[1]
            quotes.append([quote, source])
        else:
            quote = temp[0]
            quotes.append([quote, ''])
    return quotes

### root
root = tk.Tk()
root.configure(background='black')
root.attributes('-fullscreen', True)
root.call('wm', 'attributes', '.', '-topmost', True)
root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False);

### content
quotes = readQuotes()
nquotes = len(quotes)-1

now = datetime.datetime.now()
now = now.time()
now = now.isoformat()[:8]

quote = quotes[random.randint(0,nquotes)]
dataobj = ['typeOfBreak', now, quote[0], quote[1]]

root.grid_columnconfigure(0, weight=1)
W = []
for i in range(2):
    w = tk.Label(root)
    w.config(text=dataobj[i], bg='black', foreground='white', width=500, font='times 24', wraplength=1000, justify='left')
    w.grid(row=i)
    root.grid_rowconfigure(i, weight=1)
    W.append(w)

f = tk.Frame(root, bg='black')
f.grid(row=3)
root.grid_rowconfigure(3, weight=1)
w = tk.Label(f)
w.config(text=dataobj[2], bg='black', foreground='white', width=100, font='times 24', wraplength=1000, justify='left')
w.pack()
W.append(w)
w = tk.Label(f)
w.config(text=dataobj[3], bg='black', foreground='white', width=50, font='times 24', justify='right', anchor=tk.E)
w.pack()
W.append(w)


clock('short')
root.mainloop()