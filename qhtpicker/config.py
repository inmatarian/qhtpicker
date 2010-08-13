
import sys, os, logging, PyQt4
from logging import debug, info, warning, error, critical
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# --------------------------------------

class Config(dict):
  
    def __init__(self, rootdir):
        self.initDefaultKeys()
        self.loadAllKeys()
        if (not rootdir is None) and os.path.isdir(rootdir):
            self["rootdirectory"] = rootdir
            debug("arg rootdirectory: %s" % rootdir)
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
        # default handlers
        self.handlers = [ ["*.nes","fceu"] ]
        return

    def loadAllKeys(self):
        settings = QSettings()
        info("Loading keys from config file: %s" % settings.fileName())
        settings.sync()
        keys = settings.allKeys()
        for i in keys:
            s = str(i)
            if s.find("handlers") >= 0: continue # skip handlers
            self[s] = settings.value(i).toString()
            debug("[%s]=%s"%(s, self[s]))
        self.loadHandlers(settings)
        return

    def loadHandlers(self, settings):
        h = []
        n = settings.beginReadArray("handlers");
        if n == 0: return
        info("Loading %i handlers" % n)
        for i in xrange(0, n):
            settings.setArrayIndex(i);
            glob = str(settings.value("glob").toString())
            launcher = str(settings.value("launcher").toString())
            h.append( [glob, launcher] )
            debug("[handlers][%i] = glob:%s : launcher:%s" % (i, h[i][0], h[i][1]) )
        self.handlers = h
        settings.endArray()
        return

    def saveAllKeys(self):
        settings = QSettings()
        info("Saving keys to config file: %s" % settings.fileName())
        for i in self:
            s = str(self[i])
            if i == "handlers": continue # skip handlers
            settings.setValue(i, s)
            debug("[%s]=%s"%(i, s))
        self.saveHandlers(settings)
        settings.sync()
        return

    def saveHandlers(self, settings):
        h = self.handlers
        if len(h) == 0: return
        info("Saving %i handlers" % len(h))
        settings.beginWriteArray("handlers", len(h))
        for i in xrange(0, len(h)):
            settings.setArrayIndex(i)
            settings.setValue("glob", h[i][0])
            settings.setValue("launcher", h[i][1])
            debug("[handlers][%i] = glob:%s : launcher:%s" % (i, h[i][0], h[i][1]) )
        settings.endArray()
        return

