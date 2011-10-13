import threading

__author__ = 'jon'

class GoogleResultParserThread(threading.Thread):

    def __init__(self, resultDictionary):
        """
          Initialize this parser, given the dictionary into which the page's data is going to be placed
        """

        threading.Thread.__init__(self)

    