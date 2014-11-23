# -*- coding: utf-8 -*-

import alsaaudio
import gflags
import sys
import signal
import websocket

FLAGS = gflags.FLAGS

gflags.DEFINE_string("server", None, "e.g. ws://hoge:5000/audio")
gflags.DEFINE_string("card", "default", "A sound card index")
gflags.DEFINE_integer("chunk", 1024, "the period size")
gflags.DEFINE_integer("channels", 1, "the number of channel")
gflags.DEFINE_integer("rate", 44100, "the sampling rate")


FORMAT = alsaaudio.PCM_FORMAT_S16_LE
RATE = 44100

def main(argv):
    argv = gflags.FLAGS(argv)
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
            alsaaudio.PCM_NONBLOCK, FLAGS.card)

    inp.setchannels(FLAGS.channels)
    inp.setrate(FLAGS.rate)
    inp.setformat(FORMAT)

    inp.setperiodsize(FLAGS.chunk)
    ws = websocket.create_connection(FLAGS.server)

    def signal_term_handler(signal, frame):
        ws.close()
        sys.exit(0)
    signal.signal(signal.SIGTERM, signal_term_handler)

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
