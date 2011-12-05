__author__ = 'jon'

class Ranking(object):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def __init__(self, searchResults, keywords):
        """
          Creates a ranking object with the necessary parameters

            @param  searchResults   The list of search results, in the following format:
                                        [
                                            {
                                                'url': <url>
                                                'preview' : <preview snippet>
                                                'title' : <title>
                                                'description' : <meta description>
                                                'pageRank' : <PageRank, between 0 and 10>
                                                'content' : <page content>
                                            },
                                            ...
                                        ]
            @param  keywords        The keywords for these search results to use for scoring the results
        """

        self.searchResults = searchResults
        self.keywords = keywords

    def rank(self):
        raise NotImplementedError
        