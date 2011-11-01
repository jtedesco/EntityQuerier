from pprint import pprint
from src.analysis.TermFrequencyAnalysis import TermFrequencyAnalysis
from src.search.Search import Search
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class TopKKeywordSearch(Search):
    """
      This class allows us to augment results by re-querying with the top K keywords
    """

    def __init__(self, searchScheme = GoogleSearch(), numberOfResultsToRetrieve=50, verbose=True, k=10):
        """
          Initializes this search object
        """

        Search.__init__(self, numberOfResultsToRetrieve, verbose)
        self.searchScheme = searchScheme
        self.k = k


    def query(self, query, fetchContent=True):

        # Get the search results from the 'concrete' scheme
        searchResults = self.searchScheme.query(query, fetchContent)
        resultPages = list(searchResults)

        # Find the top K words from these results
        termFrequencyAnalysis = TermFrequencyAnalysis(resultPages)
        keywords = termFrequencyAnalysis.getTopKWords(self.k)

        id = query.split(" +\"")[0]
        for word in keywords:
            keywordQuery = id + ' +"%s"' % word
            searchResults.append(self.searchScheme.query(keywordQuery, fetchContent))

        return searchResults
