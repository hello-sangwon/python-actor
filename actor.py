#!/usr/bin/env python

from __future__ import print_function
from Queue import Queue
from threading import Thread, Event


class ActorExit(Exception):
    pass


class Actor(object):
    def __init__(self):
        self._mailbox = Queue()

    def send(self, msg):
        self._mailbox.put(msg)

    def recv(self):
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        self.send(ActorExit)

    def run(self):
        while True:
            msg = self.recv()
            print('Got: ', msg)

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def start(self):
        self._terminated = Event()
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()

    def join(self):
        self._terminated.wait()


class PrintActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print('print: ', msg)


if __name__ == '__main__':
    actor = PrintActor()
    actor.start()
    actor.send('Hello, actor!')
    actor.send({'name': 'sangwon', 'age': 21})
    for x in range(5):
        actor.send(x)
    actor.close()
    actor.join()

# vim: set fenc=utf8 expandtab sw=4 ts=4:
