from pprint import pprint
import threading
from time import sleep

__author__ = 'jon'

class SearchThread(threading.Thread):

    
    def __init__(self, dictionary):
        """
          Initialize this parser, given the dictionary into which the page's data is going to be placed
        """
        threading.Thread.__init__(self)

        # Pull the data out of the dictionary
        self.dictionary = dictionary
        self.entity = dictionary['entity']
        self.entityId = dictionary['entityId']
        self.trigger = dictionary['trigger']

        pprint(dictionary)

    def update(self, message):
        """
          Updates the UI saying with the given message
        """

        self.dictionary['status'] = message
        self.trigger.release()

        
    def run(self):
        """
          Run the search, and update the dictionary (releasing the lock to trigger a callback whenever one should occur)
        """

        while self.iterations < 5:

            sleep(2)

            self.iterations +=1
            message = "Iteration " + str(self.iterations)
            self.update(message)

        # Signal that we're finally done
        message = "done"
        self.update(message)

