from struct import unpack

from can import Listener
from PyQt5.QtCore import QObject, pyqtSignal


class canFrameAppender(Listener, QObject):

    frameReceived = pyqtSignal(str)

    def __init__(self, appendFunction):
        super().__init__()
        self.frameReceived.connect(appendFunction)

    def on_message_received(self, msg):
        #print (msg.data[0:3])
        #print (msg.data[4:7])
        self.frameReceived.emit("ID: {}\tDLC: {}\t{} \tNUMS:{}"
                                .format(msg.arbitration_id, msg.dlc, msg.data.hex(), unpack('ff', msg.data)))


class switchingSetter(Listener, QObject):

    frameReceived = pyqtSignal(float)

    def __init__(self, setterSlot):
        super().__init__()
        self.frameReceived.connect(setterSlot)

    def on_message_received(self, msg):
        if (msg.arbitration_id == 19):
            values = unpack('ff', msg.data)
            self.frameReceived.emit(values[0])
