
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

    def setOrigDirectoryOption(self, directory):
        self.origDirectoryOption = directory
        self.setDirectoryOption(directory)

    def setDirectoryOption(self, directory):
        self.directoryOption = directory
        self.directoryButton.setText( directory )

    def getDirectoryOption(self):
        return str(self.directoryEdit.text())

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

    @pyqtSlot("")
    def on_directoryButton_clicked(self):
        d = QFileDialog.getExistingDirectory(self, 
            "Open Directory", self.directoryOption,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks )
        if len(d) > 0: self.setDirectoryOption(d)

    def handleApplyPressed(self):
        self.applyClicked.emit()

    def setListOfHandlers(self, handlers):
        debug("adding handlers to table: %i" % len(handlers))
        self.handlersTable.setSortingEnabled(False)
        self.handlersTable.setRowCount( len(handlers) )
        for i in xrange(0, len(handlers)):
            debug("HANDLER: %s : %s" % (handlers[i][0], handlers[i][1]))
            self.handlersTable.setItem( i, 0, QTableWidgetItem(handlers[i][0]) )
            self.handlersTable.setItem( i, 1, QTableWidgetItem(handlers[i][1]) )
        return

    def getListOfHandlers(self):
        handlers = []
        n = self.handlersTable.rowCount()
        for i in xrange(0, n):
            glob = str(self.handlersTable.item( i, 0 ).text())
            launcher = str(self.handlersTable.item( i, 1 ).text())
            if len(glob)>1 and len(launcher)>1:
                handlers.append ( [ glob, launcher ] )
                debug("HANDLER: %s : %s" % (glob, launcher))
        return handlers

