
import sys, os, logging, PyQt4
from logging import debug, info, warning, error, critical
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# --------------------------------------

class PreferencesDialog(QDialog):
    applyClicked = pyqtSignal()

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        uic.loadUi("prefs.ui", self)
        self.connect( self.buttonBox.button(QDialogButtonBox.Apply),
            SIGNAL("clicked()"), self.handleApplyPressed )

    def setOrigFontOption(self, font):
        self.origFontOption = font
        self.setFontOption(font)

    def setFontOption(self, font):
        self.fontOption = font
        self.fontButton.setText( font.toString() )

    def setOrigFrontColorOption(self, color):
        self.origFrontColorOption = color
        self.setFrontColorOption(color)

    def setFrontColorOption(self, color):
        self.frontColorOption = color
        self.frontButton.setText( color.name() )

    def setOrigBackColorOption(self, color):
        self.origBackColorOption = color
        self.setBackColorOption(color)

    def setBackColorOption(self, color):
        self.backColorOption = color
        self.backButton.setText( color.name() )

    @pyqtSlot("")
    def on_fontButton_clicked(self):
        debug("on_fontButton_clicked")
        (font, ok) = QFontDialog.getFont( self.fontOption, self )
        if ok: self.setFontOption(font)

    @pyqtSlot("")
    def on_frontButton_clicked(self):
        debug("on_frontColorButton_clicked")
        color = QColorDialog.getColor( self.frontColorOption, self )
        if color.isValid(): self.setFrontColorOption(color)

    @pyqtSlot("")
    def on_backButton_clicked(self):
        debug("on_backColorButton_clicked")
        color = QColorDialog.getColor( self.backColorOption, self )
        if color.isValid(): self.setBackColorOption(color)

    @pyqtSlot("")
    def on_addButton_clicked(self):
        debug("on_addButton_clicked")
        self.handlersTable.insertRow( self.handlersTable.rowCount() )

    @pyqtSlot("")
    def on_removeButton_clicked(self):
        debug("on_deleteButton_clicked")
        selected = self.handlersTable.selectedIndexes()
        if len(selected) < 1: return
        debug("removing row %i" % selected[0].row() )
        self.handlersTable.removeRow( selected[0].row() )

    def handleApplyPressed(self):
        self.applyClicked.emit()

    def setListOfHandlers(self, handlers):
        self.handlersTable.setRowCount( len(handlers) )
        i = 0
        while i < len(handlers)
            self.handlersTable.setItem( i, 0, QTableWidgetItem(handlers[i][0]) )
            self.handlersTable.setItem( i, 1, QTableWidgetItem(handlers[i][1]) )
            i += 1
        return

    def getListOfHandlers(self):
        handlers = []
        i = 0
        n = self.handlersTable.rowCount()
        while i < n:
            x = self.handlersTable.item( i, 0 )
            c = self.handlersTable.item( i, 1 )
            if len(x.text())>1 and len(c.text())>1:
                handlers += ( x.text(), c.text()  )
            i += 1
        return tuple(handlers)

