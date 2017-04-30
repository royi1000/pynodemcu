#!/usr/bin/env python

import socket
import serial
import logging
import argparse

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
MAGIC_COOKIE = 'telnet'


class NodeMcuCommander(object):
    pass


class NodeMcuCommanderTCP(NodeMcuCommander):
    def __init__(self, ip, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((ip, port))
        self._sock.send(MAGIC_COOKIE + '\n')
        if not s.recv(1000).startswith('Welcome to NodeMCU'):
            raise OSError('NodeMCU signature not found')
        logger.info('connected')

    def __del__(self):
        self._sock.send(chr(4) + '\n')


class NodeMcuCommanderSerial(NodeMcuCommander):
    def __init__(self, dev, baud):
        logger.debug('opening serial')
        self._serial = serial.Serial(dev, baud, timeout=3)
        logger.debug('writing test cmd')
        self._serial.write('=node.heap()')
        logger.debug('reading response')
        if not self._serial.readline().startswith('=node.heap()'):
            raise OSError('NodeMCU signature not found')
        logger.debug(self._serial.readline())
        logger.info('serial connected')

def run(args):
    if args.serial:
        mcu = NodeMcuCommanderSerial(args.serial, args.baud)
    else:
        mcu = NodeMcuCommanderTCP()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NodeMCU commander parser')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("--tcp", help="tcp", action="store_true")
    parser.add_argument("--serial", help="serial dev", default='')
    parser.add_argument("--baud", help="serial baud", default=9600)
    parser.add_argument("--ip", help="NodeMCU ip", default='192.168.4.1')
    parser.add_argument("--port", help="NodeMCU port", default=80)
    args = parser.parse_args()
    run(args)
