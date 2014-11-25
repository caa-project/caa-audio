#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.web
import tornado.websocket
import threading


def synchronized(fun):
    def wrap(self, *args, **kwargs):
        with self.lock:
            return fun(self, *args, **kwargs)
    return wrap


class HandlerContainer:

    _instance = None

    def __init__(self):
        self._handlers = dict()
        self.lock = threading.Lock()

    @synchronized
    def add_recieve_handler(self, handler):
        index = handler.index
        if index not in self._handlers:
            self._handlers[index] = [handler, None]
        elif self._handlers[index][0] is None:
            self._handlers[index][0] = handler

    @synchronized
    def remove_recieve_handler(self, index):
        if index not in self._handlers:
            return
        self._handlers[index][0] = None
        if self._handlers[index] == [None, None]:
            self._handlers.pop(index)

    @synchronized
    def add_send_handler(self, handler):
        index = handler.index
        if index not in self._handlers:
            self._handlers[index] = [None, handler]
        elif self._handlers[index][1] is None:
            self._handlers[index][1] = handler

    @synchronized
    def remove_send_handler(self, index):
        if index not in self._handlers:
            return
        self._handlers[index][1] = None
        if self._handlers[index] == [None, None]:
            self._handlers.pop(index)

    def send_binary(self, index, message):
        if index not in self._handlers or self._handlers[index][1] is None:
            return
        self._handlers[index][1].write_message(message, binary=True)

    def connection(self):
        """接続状況を文字列で返す"""
        return str(self._handlers)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class SoundRecieveHandler(tornado.websocket.WebSocketHandler):

    def open(self, index):
        self.index = index
        HandlerContainer.instance().add_recieve_handler(self)

    def on_message(self, response):
        HandlerContainer.instance().send_binary(self.index, response)

    def on_close(self):
        HandlerContainer.instance().remove_recieve_handler(self.index)


class SoundSendHandler(tornado.websocket.WebSocketHandler):

    def open(self, index):
        self.index = index
        HandlerContainer.instance().add_send_handler(self)

    def on_close(self):
        HandlerContainer.instance().remove_send_handler(self.index)


class ViewConnectionHandler(tornado.web.RequestHandler):

    def get(self):
        c = HandlerContainer.instance()
        self.write(c.connection())


def start_server(port):
    app = tornado.web.Application([
        (r"/robo/([0-9a-zA-Z]+)", SoundRecieveHandler),
        (r"/user/([0-9a-zA-Z]+)", SoundSendHandler),
        (r"/connection", ViewConnectionHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
