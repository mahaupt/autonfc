import ctypes
from ctypes import *
import cv2
from pyzbar import pyzbar
import validators
import ndef
import ErrorCodes
from main import uFR

def getQRData(img):
  barcodes = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
  if len(barcodes) == 0:
    cv2.bitwise_not(img, img) #invert color
    barcodes = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
  
  for barcode in barcodes:
    if barcode.type == "QRCODE":
      url = barcode.data.decode("utf-8")
      if validators.url(url):
        return url, False
      else:
        print("error: qr code does not contain valid url")
        return False, True
  return False, False

def ReaderUISignal(light, sound):
    uiSignal = uFR.ReaderUISignal
    uiSignal.argtypes = (c_ubyte, c_ubyte)
    uiSignal.restype = c_uint
    uiSignal(light, sound)

def InitCard():
    status = uFR.ndef_card_initialization()
    if status == 0:
        print("Card initialized succesfully.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        return True
    else:
        print("Card initialization failed.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        return False


def WriteNFC(uri):
  record = ndef.UriRecord(uri)
  payload_tmp = b''.join(ndef.message_encoder([record]))
  payload_tmp = payload_tmp[4:] # skip first 4 bytes
  payload_length = c_uint32(len(payload_tmp))
  payload = (c_ubyte * len(payload_tmp)).from_buffer_copy(payload_tmp)

  message_nr = c_ubyte(1)
  tnf = c_ubyte(1)
  type_record = c_ubyte(85)  # 'U'
  type_length = c_ubyte(1)
  id = (c_ubyte*2)()
  id_length = c_ubyte(0)
  card_formatted = c_ubyte()

  writeNdefFunc = uFR.write_ndef_record
  writeNdefFunc.argtypes = [c_ubyte,  POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_ubyte), (c_ubyte*2), POINTER(c_ubyte), (c_ubyte*payload_length.value), POINTER(c_uint32), POINTER(c_ubyte)]

  status = writeNdefFunc(message_nr, byref(tnf), byref(type_record), byref(type_length), id, byref(id_length), payload, byref(payload_length), byref(card_formatted))
  if status == 0:
    print("URI NDEF written successfully.")
    print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    return True
  else:
    print("URI NDEF write failed.")
    print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    return False




