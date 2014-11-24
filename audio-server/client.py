# -*- coding: utf-8 -*-

import gflags
import websocket
import datetime
import time
import wave
import pyaudio
import sys

FLAGS = gflags.FLAGS

gflags.DEFINE_float("delay", 0.1, "the initial delay")
gflags.DEFINE_string("server", None, "the server address")
gflags.DEFINE_integer("rate", 44100, "the sampling rate")
# Typical values => 8000(telephone), 16000,  44100(CD), 96000

def main(argv):
    argv = gflags.FLAGS(argv)

    FORMAT = pyaudio.paInt16
    RATE = FLAGS.rate

    p = pyaudio.PyAudio()
    stream = p.open(
            format=FORMAT,
            channels=1,
            rate=RATE,
            output=True)

    initial_delay_sec = datetime.timedelta(seconds=FLAGS.delay);

    def on_message(ws, message):
        current_time = datetime.datetime.now()
        sleep_time = 0.5/RATE*len(message)
        duration = datetime.timedelta(seconds=sleep_time)
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
            ws = websocket.WebSocketApp(FLAGS.server,
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

if __name__ == '__main__':
    main(sys.argv)
