# -*- coding: utf-8 -*-

import alsaaudio
import gflags
import websocket

FLAGS = gflags.FLAGS

gflags.DEFINE_string("server", None, "URL to audio-server.")
gflags.DEFINE_string("index", None, "Index of this robot.")


PERIODSIZE = 1024   # CHUNK
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)

inp.setchannels(CHANNELS)
inp.setrate(RATE)
inp.setformat(FORMAT)

inp.setperiodsize(PERIODSIZE)

ws = websocket.create_connection(
    'ws://%s/robo/%s' % (FLAGS.server, FLAGS.index))

while True:
    l, data = inp.read()
    ws.send_binary(data)

ws.close()
inp.pause()
