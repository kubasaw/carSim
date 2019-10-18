from PyQt5 import QtCore


class tableGuiConnector(QtCore.QAbstractTableModel):
    def __init__(self, myTab):
        self.__internalTable = myTab
        super().__init__()

    def rowCount(self, parent):
        return len(self.__internalTable)

    def columnCount(self, parent):
        return int(2)

    def data(self, index, role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return self.__internalTable[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Position"
            else:
                return "Height"
        if orientation == QtCore.Qt.Vertical:
            return section

    def flags(self,index):
        return QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable

    def setData(self,index,value,role):
        if role!=QtCore.Qt.EditRole:
            return False
        try:
            self.__internalTable[index.row()][index.column()]=float(value)
        except:
            return False
        return True

    def insertRows(self, row, count=1, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent,row,row+count-1)

        for i in range(0,count):
            self.__internalTable.insert(row,[0]*2)

        self.endInsertRows()

        return True

    def removeRows(self, row, count=1, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent,row,row+count-1)

        for i in range(row,row+count):
            self.__internalTable.pop(i)

        self.endRemoveRows()

        return True
    


    

    
