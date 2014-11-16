# -*- coding: utf-8 -*-

import alsaaudio
import gflags
import sys
import websocket

FLAGS = gflags.FLAGS

gflags.DEFINE_string("server", None, "e.g. ws://hoge:5000/audio")


PERIODSIZE = 1024   # CHUNK
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5


def main(argv):
    argv = gflags.FLAGS(argv)
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)

    inp.setchannels(CHANNELS)
    inp.setrate(RATE)
    inp.setformat(FORMAT)

    inp.setperiodsize(PERIODSIZE)

    ws = websocket.create_connection(FLAGS.server)

    while True:
        l, data = inp.read()
        ws.send_binary(data)

    ws.close()
    inp.pause()

if __name__ == '__main__':
    main(sys.argv)
