# -*- coding: utf-8 -*-

import alsaaudio
import gflags
import sys
import signal
import websocket

FLAGS = gflags.FLAGS

gflags.DEFINE_string("server", None, "e.g. ws://hoge:5000/audio")
gflags.DEFINE_string("card", "default", "A sound card index")


PERIODSIZE = 1024*4   # CHUNK
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
#FORMAT = alsaaudio.PCM_FORMAT_FLOAT_LE
CHANNELS = 1
RATE = 44100

def main(argv):
    argv = gflags.FLAGS(argv)
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
            alsaaudio.PCM_NONBLOCK, FLAGS.card)

    inp.setchannels(CHANNELS)
    inp.setrate(RATE)
    inp.setformat(FORMAT)

    inp.setperiodsize(PERIODSIZE)
    ws = websocket.create_connection(FLAGS.server)

    def signal_term_handler(signal, frame):
        ws.close()
        sys.exit(0)

    try:
        while True:
            l, data = inp.read()
            if l <= 0:
                continue
            ws.send_binary(data)
    except KeyboardInterrupt:
        ws.close()

if __name__ == '__main__':
    main(sys.argv)
