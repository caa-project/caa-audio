#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gflags
import os
import server

gflags.DEFINE_integer("port", None, "port number the server listen on")

def main(argv):
    argv = gflags.FLAGS(argv)

    if gflags.FLAGS.port is None:
        port = int(os.environ.get("PORT", 5000))
    else:
        port = gflags.FLAGS.port
    server.start_server(port)

if __name__ == '__main__':
    main(sys.argv)
