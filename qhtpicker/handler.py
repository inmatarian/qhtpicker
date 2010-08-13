
import os, sys, logging, fnmatch, subprocess
from logging import debug, info, warning, error, critical

# --------------------------------------

class Handler(object):
    def __init__(self, config):
        self.config = config

    def launch(self, filename, launcher):
        info("Launching %s" % filename)
        cmdline = launcher.split(" ")
        cmdline.append(filename)
        debug("Command Line: %s" % cmdline)
        subprocess.Popen(cmdline)
        return

    def handle(self, filename):
        debug("Handling %s" % filename)
        for i in self.config.handlers:
            glob = i[0]
            launcher = i[1]
            if fnmatch.fnmatch(filename, glob):
                self.launch(filename, launcher)
                return
        return

# --------------------------------------

if __name__ == "__main__":
    logging.basicConfig( level=logging.DEBUG,
                         format="%(levelname)s: %(message)s" )
    h = Handler( "stevejobssucks" )
    h.handle( sys.argv[1] )

