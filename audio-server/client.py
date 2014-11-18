# -*- coding: utf-8 -*-

import websocket
import datetime
import time
import wave
import pyaudio
import sys

if len(sys.argv) < 2:
    print >> sys.stderr, "Require 2 parameters: server_address and index"
    sys.exit(1)

host = sys.argv[1]
index = sys.argv[2]

FORMAT = pyaudio.paInt16
#FORMAT = pyaudio.paFloat32
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(
        format=FORMAT,
        channels=1,
        rate=RATE,
        output=True)

initial_delay_sec = datetime.timedelta(seconds=2.0);

def on_message(ws, message):
    current_time = datetime.datetime.now()
    duration = datetime.timedelta(seconds=1.0/RATE*len(message)/2)
    if current_time < ws.scheduled_time:
        time.sleep((ws.scheduled_time - current_time).total_seconds())
        stream.write(message)
        ws.scheduled_time += duration
    else:
        stream.write(message)
        ws.scheduled_time = current_time + duration + initial_delay_sec

def on_close(ws):
    print '[on close]'

def on_open(ws):
    print '[on open]'

while True:
    try:
        ws = websocket.WebSocketApp('ws://%s/user/%s' % (host, index),
                on_message=on_message,
                on_close=on_close)
        ws.scheduled_time = datetime.datetime.now() + initial_delay_sec
        ws.on_open = on_open
        ws.run_forever()
        time.sleep(1)
    except KeyboardInterrupt:
        break

ws.close()
stream.stop_stream()
stream.close()
p.terminate()
