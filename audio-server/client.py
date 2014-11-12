# -*- coding: utf-8 -*-

import websocket
import time
import wave
import pyaudio

# host = 'localhost'
# port = 5000
host = 'benijake-sound-server.herokuapp.com'
port = 80
index = 1024

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(
        format=FORMAT,
        channels=1,
        rate=RATE,
        output=True)

def on_message(ws, message):
    stream.write(message)

def on_close(ws):
    print '[on close]'

def on_open(ws):
    print '[on open]'

while True:
    try:
        ws = websocket.WebSocketApp('ws://%s:%s/user/%s' % (host, port, index),
                on_message=on_message,
                on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
        time.sleep(1)
    except KeyboardInterrupt:
        break

ws.close()
stream.stop_stream()
stream.close()
p.terminate()
