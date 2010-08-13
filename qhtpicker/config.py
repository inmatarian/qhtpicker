
import sys, os, logging, PyQt4
from logging import debug, info, warning, error, critical
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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

