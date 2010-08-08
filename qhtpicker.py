#!/usr/bin/python

import sys, os, logging
from logging import debug, info, warning, error, critical
from PyQt4 import QtCore, QtGui

class QHTPicker(QtGui.QWidget):
    def __init__(self, config, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.config = config
        self.setWindowTitle("QHTPicker")

        self.filemodel = QtGui.QFileSystemModel(self)
        self.filemodel.setRootPath("/")
        self.filelist = QtGui.QTreeView(self)
        self.filelist.setModel(self.filemodel)
        self.filelist.setRootIndex(self.filemodel.index(config.rootdirectory));

        self.filelist.setHeaderHidden(True)
        cols = self.filemodel.columnCount()
        for i in xrange(1, cols):
            self.filelist.hideColumn(i)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.filelist)
        self.setLayout(vbox)
        qdw = QtGui.QDesktopWidget()
        rect = qdw.screenGeometry()
        desiredHeight = rect.height() / 12
        font = self.font()
        font.setPixelSize( desiredHeight )
        self.setFont(font)
        self.show()

    def closeEvent(self, event):
        event.accept()
        return

# --------------------------------------

class Config(dict):
  
    def __init__(self, argv):
        self.initDefaultKeys()
        settings = QtCore.QSettings(QtCore.QSettings.IniFormat,
                                    QtCore.QSettings.UserScope,
                                    "qhtpicker", "qhtpicker" )
        debug( "QSetting Filename: %s" % settings.fileName() )
        self.loadAllKeys()
        if len(argv) > 1:
            self["rootdirectory"] = argv[1]
        return

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key]=value

    def initDefaultKeys(self):
        defaults = ( ( "rootdirectory", "/" ), ( "foo", "bar" ) )
        for i in defaults:
            debug(i)
            self[ i[0] ] = i[1]
        return

    def loadAllKeys(self):
        settings = QtCore.QSettings()
        settings.sync()
        keys = settings.allKeys()
        for i in keys:
            self[i] = settings.value(i)
        return

    def saveAllKeys(self):
        settings = QtCore.QSettings()
        for i in self:
            settings.setValue(i,self[i])
        settings.sync()
        return

# --------------------------------------

def main():
    logging.basicConfig( level=logging.DEBUG,
                         format="%(levelname)s: %(message)s" )
    app = QtGui.QApplication(sys.argv)
    cwd = os.getcwd()
    config = Config(sys.argv)
    widget = QHTPicker(config)
    ret = app.exec_()
    config.saveAllKeys()
    os.chdir(cwd)
    sys.exit(ret)

if __name__ == "__main__":
    main()

