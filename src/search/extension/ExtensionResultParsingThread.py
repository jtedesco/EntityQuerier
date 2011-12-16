import threading
from urllib2 import URLError
import sys

__author__ = 'jon'

class ExtensionResultParserThread(threading.Thread):

    def __init__(self, resultDictionary, verbose=False, extensions=[]):
        """
          Initialize this parser, given the dictionary into which the page's data is going to be placed
        """
        threading.Thread.__init__(self)
        self.verbose = verbose
        self.resultDictionary = resultDictionary
        self.url = resultDictionary['url']
        self.extensions = extensions

        
    def run(self):
        """
          Update the result for the extensions
        """

        try:
            
            # Run the extensions
            for extension in self.extensions:
                extension.run(self.resultDictionary)

        except URLError:

            # Skip this URL, and register it as an error on the cache
            if self.verbose:
                print("Error accessing '%s', %s" % (self.url.strip(), str(sys.exc_info()[1]).strip()))
