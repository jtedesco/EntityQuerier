__author__ = 'jon'


class SearchFacade(object):
    """
      Represents an interface to a search engine. This contains methods that are not specific to any particular search
        engine, but rather ones that can be used for any.
    """

    def __init__(self, numberOfResultsToRetrieve, verbose=False, extensions=[], cache=True):
        """
          Initializes this search object,
        """
        self.verbose = verbose
        self.numberOfResultsToRetrieve = numberOfResultsToRetrieve
        self.extensions = extensions
        self.cache = cache

        
    def query(self, query):
        """
          Query the search interface and return a dictionary of results

            @param  query           The query to search
        """
        
        raise NotImplementedError("Must instantiate a concrete SearchInterface!")