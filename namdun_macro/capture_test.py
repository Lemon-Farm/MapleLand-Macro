from ultralytics import YOLO
import cv2
from mss import mss
import numpy as np
import pyautogui

model = YOLO("C:/Users/fnf00/Desktop/conda/runs/detect/train/weights/best.pt")
region = (0, -7, 1296, 759)
# sct = mss()
# monitor = {"top": 8, "left": 8, "width": 1936, "height": 1056}


# 기존 BGR파일을 RGB파일로 변경(RGB파일만 사용 가능)
# frame = np.array(sct.grab(monitor))
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = pyautogui.screenshot(region=region)
result = model(frame, save=True)
