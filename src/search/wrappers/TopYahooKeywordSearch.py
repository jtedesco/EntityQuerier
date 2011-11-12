from src.analysis.TermFrequencyAnalysis import TermFrequencyAnalysis
from src.search.Search import Search
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class TopYahooKeywordSearch(Search):
    """
      This class allows us to augment results by re-querying with the top keywords from the entire search process
        using Yahoo's YQL to extract t
    """

    def __init__(self, searchScheme = GoogleSearch(), numberOfResultsToRetrieve=50, verbose=True):
        """
          Initializes this search object
        """

        Search.__init__(self, numberOfResultsToRetrieve, verbose)
        self.searchScheme = searchScheme


    def query(self, query, fetchContent=True):
        """
          Query the search interface and return a dictionary of results

            @param  query           The query to search
            @param  fetchContent    Whether or not to retrieve the content of pages as well as just summaries + urls from google
            @param  lastQuery       Whether or not this query is the last that will be submitted for the search process
        """

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
