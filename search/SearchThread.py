import threading
from time import sleep

__author__ = 'jon'

class SearchThread(threading.Thread):

    
    def __init__(self, dictionary):
        """
          Initialize this parser, given the dictionary into which the page's data is going to be placed
        """
        threading.Thread.__init__(self)
        self.dictionary = dictionary
        self.query = dictionary['query']
        self.trigger = dictionary['trigger']

        self.iterations = 0


    def run(self):
        """
          Run the search, and update the dictionary (releasing the lock to trigger a callback whenever one should occur)
        """

        while self.iterations < 5:

            sleep(2)

            self.iterations +=1
            self.dictionary['status'] = "Iteration " + str(self.iterations)
            self.trigger.release()

        # Signal that we're finally done
        self.dictionary['status'] = "done"
        self.trigger.release()

