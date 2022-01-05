import ctypes
from ctypes import *
from Functions import *
import cv2
import time
from pyzbar import pyzbar

##########################################################################
# dll loading
uFR = cdll.LoadLibrary("ufr-lib//linux//aarch64//libuFCoder-aarch64.so")
##########################################################################

if __name__ == '__main__':

  # start video / open webcam
  cap = cv2.VideoCapture(0)
  time.sleep(3)
  if cap.isOpened():
    print("webcam opened")
  else:
    print("error: could not open webcam")
    exit(-1)

  # open nfc reader/writer
  status = uFR.ReaderOpen()
  if status == 0:
    print("nfc reader opened")
  else:
    print("error: could not open nfc reader")
    exit(-1)
  ReaderUISignal(1, 2)

  # main loop
  lastDetected = ""
  lastDetectedTimeout = 10
  while True:
    _, img = cap.read()
    for x in range(10):
      _, img = cap.read() # empty buffer
    cv2.resize(img, (1024, 768))

    # get qr data
    data, err = getQRData(img)
    if err:
      ReaderUISignal(4, 0)
      continue

    # write nfc
    if data and data != lastDetected:
      print("QR Data:" + data)
      lastDetected = data
      lastDetectedTimeout = 10
      if InitCard():
        if WriteNFC(data):
          ReaderUISignal(1, 1) #success
          continue
      ReaderUISignal(2, 4) #failed
    else:
      lastDetectedTimeout -= 1
      if lastDetectedTimeout <= 0:
        lastDetected = ""

  uFR.ReaderClose()





