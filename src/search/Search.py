__author__ = 'jon'


class Search(object):
    """
      Represents an interface to a search engine. This contains methods that are not specific to any particular search
        engine, but rather ones that can be used for any.
    """

    def query(self, query, numberOfResults=10, fetchContent=True):
        """
          Query the search interface and return a dictionary of results
        """
        
        raise NotImplementedError("Must instantiate a concrete SearchInterface!")