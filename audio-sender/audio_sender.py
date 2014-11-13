# -*- coding: utf-8 -*-

import alsaaudio
import websocket

HOST = '==INPUT YOUR SERVER ADDRESS=='
INDEX = 1024

PERIODSIZE = 1024 # CHUNK
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)

inp.setchannels(CHANNELS)
inp.setrate(RATE)
inp.setformat(FORMAT)

inp.setperiodsize(PERIODSIZE)

ws = websocket.create_connection('ws://%s/robo/%s' % (HOST, INDEX))

while True:
    l, data = inp.read()
    ws.send_binary(data)

ws.close()
inp.pause()
