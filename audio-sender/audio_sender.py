# -*- coding: utf-8 -*-

import alsaaudio
import gflags
import sys
import signal
import websocket
import time

FLAGS = gflags.FLAGS

gflags.DEFINE_string("server", None, "e.g. ws://hoge:5000/audio")
gflags.DEFINE_string("card", "default", "A sound card index")
gflags.DEFINE_integer("chunk", 1024, "the period size")
gflags.DEFINE_integer("channels", 1, "the number of channel")
gflags.DEFINE_integer("rate", 44100, "the sampling rate")
# Typical values => 8000(telephone), 16000,  44100(CD), 96000


FORMAT = alsaaudio.PCM_FORMAT_S16_LE


def main(argv):
    argv = gflags.FLAGS(argv)
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                        alsaaudio.PCM_NONBLOCK, FLAGS.card)

    inp.setchannels(FLAGS.channels)
    inp.setrate(FLAGS.rate)
    inp.setformat(FORMAT)

    inp.setperiodsize(FLAGS.chunk)

    ws = None

    def signal_term_handler(signal, frame):
        ws.close()
        sys.exit(0)
    signal.signal(signal.SIGTERM, signal_term_handler)

    while True:
        try:
            ws = websocket.create_connection(FLAGS.server)
            while ws.connected:
                l, data = inp.read()
                if l <= 0:
                    continue
                ws.send_binary(data)
        except KeyboardInterrupt:
            ws.close()
            break
        except:
            time.sleep(1)  # wait for reconnecting

if __name__ == '__main__':
    main(sys.argv)
