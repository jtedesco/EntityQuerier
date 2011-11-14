__author__ = 'jon'

class Extension(object):
    """
      Implements a generic interface for extensions that can be added to the parser threads
    """

    def run(self, resultDictionary):
        raise NotImplementedError("Must instantiate an extension object to run!")