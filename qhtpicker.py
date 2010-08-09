#!/usr/bin/python

import sys, os, logging, PyQt4
from logging import debug, info, warning, error, critical
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QHTPicker(QWidget):
    def __init__(self, config, handler, parent=None):
        info("Initializing QHTPicker Widget")
        QWidget.__init__(self, parent)
        self.config = config
        self.handler = handler
        self.setWindowTitle("QHTPicker")

        self.filemodel = QFileSystemModel(self)
        self.filemodel.setRootPath("/")
        self.filelist = QTreeView(self)
        self.filelist.setModel(self.filemodel)
        debug("using rootdirectory: %s" % config.rootdirectory)
        self.filelist.setRootIndex(self.filemodel.index(config.rootdirectory));

        self.filelist.setHeaderHidden(True)
        cols = self.filemodel.columnCount()
        for i in xrange(1, cols):
            self.filelist.hideColumn(i)

        self.connect( self.filelist,
                      SIGNAL("activated(const QModelIndex &)"),
                      self.handleActivated )

        vbox = QVBoxLayout()
        vbox.addWidget(self.filelist)
        self.setLayout(vbox)


        self.fontAction = QAction("Change Font", self)
        self.connect( self.fontAction, SIGNAL("triggered()"), self.handleFontAction )
        self.addAction( self.fontAction )
        quitsep = QAction(self)
        quitsep.setSeparator(True)
        self.addAction(quitsep)
        self.quitAction = QAction("Quit", self)
        self.quitAction.setMenuRole( QAction.QuitRole )
        self.connect( self.quitAction, SIGNAL("triggered()"), self, SLOT("close()") )
        self.addAction( self.quitAction )
        self.setContextMenuPolicy( Qt.ActionsContextMenu )

        if "font" in config and not config.font == None:
            font = QFont()
            font.fromString(config.font)
        else:
            qdw = QDesktopWidget()
            rect = qdw.screenGeometry()
            desiredHeight = rect.height() / 12
            font = self.font()
            font.setPixelSize( desiredHeight )
        self.setFont(font)
        debug(font.toString())
        (uw, uh, ux, uy) = ( int(self.config["window/xsize"]),
                             int(self.config["window/ysize"]),
                             int(self.config["window/xpos"]),
                             int(self.config["window/ypos"]) )
        self.setGeometry(ux, uy, uw, uh)
        debug("Positioning at (%i,%i) %ix%i" % (ux, uy, uw, uh) )
        self.show()
        
    def closeEvent(self, event):
        g = self.geometry()
        self.config["window/xsize"] = g.width()
        self.config["window/ysize"] = g.height()
        self.config["window/xpos"] = g.x()
        self.config["window/ypos"] = g.y()
        self.config["font"] = self.font().toString()
        event.accept()
        return

    @pyqtSlot("const QModelIndex &")
    def handleActivated(self, index):
        fileinfo = self.filemodel.fileInfo(index)
        if fileinfo.isDir(): return
        if not fileinfo.isReadable(): return
        self.handler.handle(fileinfo.filePath())
        return

    def handleFontAction(self):
        (font, ok) = QFontDialog.getFont( self.font(), self )
        if ok: self.setFont(font)

# --------------------------------------

class Handler(object):
    def __init__(self, config):
        self.config = config

    def handle(self, filename):
        debug("Handling %s" % filename)

# --------------------------------------

class Config(dict):
  
    def __init__(self, argv):
        self.initDefaultKeys()
        self.loadAllKeys()
        if len(argv) > 1:
            self["rootdirectory"] = argv[1]
            debug("arg rootdirectory: %s" % argv[1])
        return

    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, value):
        self[key]=value

    def initDefaultKeys(self):
        info("Initializing default keys")
        defaults = ( ( "rootdirectory", "~/" ),
                     ( "window/xpos",  "0" ),
                     ( "window/ypos",  "0" ),
                     ( "window/xsize",  "250" ),
                     ( "window/ysize",  "150" ) )
        for i in defaults:
            self[ i[0] ] = i[1]
            debug("[%s]=%s"%(i[0], self[i[0]]))
        return

    def loadAllKeys(self):
        settings = QSettings()
        info("Loading keys from config file: %s" % settings.fileName())
        settings.sync()
        keys = settings.allKeys()
        for i in keys:
            s = str(i)
            self[s] = settings.value(i).toString()
            debug("[%s]=%s"%(s, self[s]))
        return

    def saveAllKeys(self):
        settings = QSettings()
        info("Saving keys to config file: %s" % settings.fileName())
        for i in self:
            settings.setValue(i, self[i])
            debug("[%s]=%s"%(i, self[i]))
        settings.sync()
        return

# --------------------------------------

def main():
    logging.basicConfig( level=logging.DEBUG,
                         format="%(levelname)s: %(message)s" )
    app = QApplication(sys.argv)
    QCoreApplication.setOrganizationName("qhtpicker");
    QCoreApplication.setApplicationName("qhtpicker");
    QSettings.setDefaultFormat(QSettings.IniFormat)
    cwd = os.getcwd()
    config = Config(sys.argv)
    handler = Handler(config)
    widget = QHTPicker(config, handler)
    ret = app.exec_()
    config.saveAllKeys()
    os.chdir(cwd)
    sys.exit(ret)

if __name__ == "__main__":
    main()

