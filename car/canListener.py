from struct import unpack

import serial
from PyQt5.QtCore import QObject, pyqtSignal


# class canFrameAppender(Listener, QObject):
#
#    frameReceived = pyqtSignal(str)
#
#    def __init__(self, appendFunction):
#        super().__init__()
#        self.frameReceived.connect(appendFunction)
#
#    def on_message_received(self, msg):
#        #print (msg.data[0:3])
#        #print (msg.data[4:7])
#        self.frameReceived.emit("ID: {}\tDLC: {}\t{} \tNUMS:{}"
#                                .format(msg.arbitration_id, msg.dlc, msg.data.hex(), unpack('ff', msg.data)))


# class switchingSetter(Listener, QObject):
#
#    frameReceived = pyqtSignal(float)
#
#    def __init__(self, setterSlot):
#        super().__init__()
#        self.frameReceived.connect(setterSlot)
#
#    def on_message_received(self, msg):
#        if (msg.arbitration_id == 19):
#            values = unpack('ff', msg.data)
#            self.frameReceived.emit(values[0])

class myCan(QObject):

    appendFrameToLog = pyqtSignal(str)
    setThrottle = pyqtSignal(float)

    def __init__(self, serialPortName):
        super().__init__()
        self.__serialhandle = serial.Serial(serialPortName, 115200)
        self.__serialhandle.reset_input_buffer()
        self.__serialhandle.reset_output_buffer()
        self.__serialhandle.write(b'C\r')
        chars = self.__serialhandle.read()
        if chars != b'\r':
            raise OSError('Bad char!')
        self.__serialhandle.write(b'S2\r')
        chars = self.__serialhandle.read()
        if chars != b'\r':
            raise OSError('Bad char!')
        self.__serialhandle.write(b'O\r')
        chars = self.__serialhandle.read()
        if chars != b'\r':
            raise OSError('Bad char!')

        self.__messageBuffer = bytes()

    def __del__(self):
        self.__serialhandle.write(b'C\r')
        self.__serialhandle.close()

    def readSerial(self):
        print("LEN: "+str(len(self.__messageBuffer)))

        while self.__serialhandle.in_waiting:
            self.__messageBuffer = self.__messageBuffer+self.__serialhandle.read()

        self.__parseForMsg()

    def __parseForMsg(self):
        while(1):
            (frame, sep, after)=self.__messageBuffer.partition(b'\r')
            if not sep:
                break
            else:
                frame=frame.decode()
                id = int(frame[1:4],16)
                dlc = int(frame[4])
                #print(dlc)
                data=[]
                for i in range(dlc):
                    data.append(int(frame[5 + i * 2:7 + i * 2], 16))
                messageReceived=canMsg(id,data)
                print(messageReceived)
                self.__messageBuffer=after

    def sendMsg(self, msg):
        self.__serialhandle.write(b't')
        # print(msg.stdId)
        # print('{:03x}'.format(msg.stdId))
        self.__serialhandle.write('{:03X}'.format(msg.stdId).encode())
        self.__serialhandle.write('{:d}'.format(len(msg.data)).encode())
        for sign in msg.data:
            self.__serialhandle.write('{:02X}'.format(sign).encode())
        self.__serialhandle.write(b'\r')


class canMsg():

    def __init__(self, StdId, Data):
        self.stdId = StdId
        self.data = Data

    def __str__(self):
        return "ID: {ID:#x}\t Data: {Data}".format(Data=[hex(no) for no in self.data], ID=self.stdId)
