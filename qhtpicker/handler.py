
import os, sys, logging
from logging import debug, info, warning, error, critical

# --------------------------------------

def getFileExtention( filename ):
    return filename.split(".")[-1]

class Handler(object):
    def __init__(self, config):
        self.config = config

    def handle(self, filename):
        debug("Handling %s" % filename)

# --------------------------------------

if __name__ == "__main__":
    logging.basicConfig( level=logging.DEBUG,
                         format="%(levelname)s: %(message)s" )
    h = Handler( "stevejobs" )
    h.handle( sys.argv[1] )

