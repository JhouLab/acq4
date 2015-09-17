"""
Driver for communicating with Scientifica PatchStar by serial interface.
"""
from __future__ import division
import serial, struct, time, collections
import numpy as np

from acq4.util.Mutex import RecursiveMutex as RLock
from ..SerialDevice import SerialDevice, TimeoutError, DataError


class PatchStar(SerialDevice):
    """
    Provides interface to a PatchStar manipulator.

    Example::

        dev = PatchStar('com4')
        print dev.getPos()
        dev.moveTo([10e-3, 0, 0], 'fast')
    """

    def __init__(self, port):
        self.lock = RLock()
        self.port = port
        SerialDevice.__init__(self, port=self.port, baudrate=9600)

    def getFirmwareVersion(self):
        with self.lock:
            self.write('DATE\r')
            return self.readUntil('\r').partition(' ')[2].partition('\t')[0]

    def getPos(self):
        """Get current manipulator position reported by controller (in micrometers).
        """
        with self.lock:
            ## request position
            self.write('POS\r')
            packet = self.readUntil('\r')
            return [int(x) for x in packet.split('\t')]

    def getSpeed(self):
        """Return the manipulator's maximum speed in micrometers per second.
        """
        with self.lock:
            self.write('TOP\r')
            return int(self.readUntil('\r'))

    def setSpeed(self, speed):
        """Set the maximum move speed in micrometers per second.
        """
        with self.lock:
            speed = int(speed)
            self.write('TOP %d\r' % speed)
            self.readUntil('\r')

    def moveTo(self, pos, speed=None):
        """Set the position of the manipulator.
        
        *pos* must be a list of 3 items, each is either an integer representing the desired position
        of the manipulator (in micrometers), or None which indicates the axis should not be moved.

        If *speed* is given, then the maximum speed of the manipulator is set before initiating the move.

        This method returns immediately. Use isMoving() to determine whether the move has completed.
        If the manipulator is already moving, then this method will time out and the command will be ignored.
        """
        with self.lock:
            currentPos = self.getPos()

            # fill in Nones with current position
            for i in range(3):
                if pos[i] is None:
                    pos[i] = currentPos[i]

            if speed is None:
                speed = self.getSpeed()
            else:
                self.setSpeed(speed)


            # Send move command
            self.write(b'ABS %d %d %d\r' % tuple(pos))
            self.readUntil('\r')

    def stop(self):
        """Stop moving the manipulator.
        """
        with self.lock:
            self.write('STOP\r')
            self.readUntil('\r')

    def isMoving(self):
        """Return True if the manipulator is moving.
        """
        with self.lock:
            self.write('S\r')
            return int(self.readUntil('\r')) != 0

    def reset(self):
        with self.lock:
            self.write('RESET\r')
            self.readUntil('\r')

