from can import Listener
from PyQt5.QtCore import pyqtSignal, QObject

class canFrameAppender(Listener, QObject):

    frameReceived = pyqtSignal(str)

    def __init__(self,appendFunction):
        super().__init__()
        self.frameReceived.connect(appendFunction)

    def on_message_received(self,msg):
        self.frameReceived.emit("ID: {}\tDLC: {}\t{}".format(msg.arbitration_id,msg.dlc,msg.data.hex()))
