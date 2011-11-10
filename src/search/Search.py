__author__ = 'jon'


class Search(object):
    """
      Represents an interface to a search engine. This contains methods that are not specific to any particular search
        engine, but rather ones that can be used for any.
    """

    def __init__(self, numberOfResultsToRetrieve=10, verbose=False):
        """
          Initializes this search object,
        """
        self.verbose = verbose
        self.numberOfResultsToRetrieve = numberOfResultsToRetrieve

        
    def query(self, query, fetchContent=True):
        """
          Query the search interface and return a dictionary of results

            @param  query           The query to search
            @param  fetchContent    Whether or not to retrieve the content of pages as well as just summaries + urls from google
        """
        
        raise NotImplementedError("Must instantiate a concrete SearchInterface!")