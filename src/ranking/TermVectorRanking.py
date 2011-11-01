import operator
from src.analysis.TermFrequencyAnalysis import TermFrequencyAnalysis

__author__ = 'jon'

class TermVectorRanking(object):
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
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        # Score the results
        scoredResults = {}
        for searchResult in self.searchResults:

            # Get the TF information for the content
            contentAnalysis = TermFrequencyAnalysis([searchResult])
            searchResultScore = 0
            for keyword in self.keywords:
                searchResultScore += contentAnalysis.getWordScore(keyword)

            scoredResults[searchResult['url']] = (searchResultScore, searchResult)

        # Re-rank the urls
        reRankedResults = []
        sortedResults = sorted(scoredResults.iteritems(), key=operator.itemgetter(1), reverse=True)
        for result in sortedResults:
            reRankedResults.append(result[1])

        return reRankedResults
        