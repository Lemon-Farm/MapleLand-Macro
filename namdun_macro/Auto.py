import pyautogui
import time
import keyboard
import numpy as np
import threading

color = (190, 190, 190)
mpos = (662, 1016)
hpos = (474, 1016)
interval = 1
toggle = False

def Toggler() :
  global toggle
  toggle = not toggle
  print("현재 상태 : ", str(toggle))

def Mauto() :
  while True :
    while not toggle : time.sleep(0.5)
    nowcolor = pyautogui.pixel(mpos[0], mpos[1])
    if (nowcolor == color) :
      pyautogui.press('2')
    time.sleep(1)
    
def Hauto() :
  while True :
    while not toggle : time.sleep(0.5)
    nowcolor = pyautogui.pixel(hpos[0], hpos[1])
    if (nowcolor == color) :
      pyautogui.press('1')
    time.sleep(1)

def Gauto() :
  while True :
    while not toggle : time.sleep(0.5)
    pyautogui.keyDown('g')
    time.sleep(0.5)
    pyautogui.keyUp('g')

mthread = threading.Thread(target= Mauto)
hthread = threading.Thread(target= Hauto)
Gthread = threading.Thread(target= Gauto)

mthread.start()
hthread.start()
Gthread.start()

while True :
  if keyboard.is_pressed('`') :
    Toggler()
  time.sleep(0.5)