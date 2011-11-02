import operator
from pprint import pprint
from src.analysis.TermFrequencyAnalysis import TermFrequencyAnalysis
from src.ranking.TermVectorRanking import TermVectorRanking

__author__ = 'jon'

class PageRankTermVectorRanking(TermVectorRanking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def score(self, searchResult):
        """
          Score the result by summing word scores, then combining the total with the page's
            page rank.
        """


        # Get the TF information for the content
        contentAnalysis = TermFrequencyAnalysis([searchResult])
        searchResultScore = 0
        for keyword in self.keywords:
            searchResultScore += contentAnalysis.getWordScore(keyword)
        searchResultScore = searchResultScore + float(searchResult['pageRank']) / 10

        return searchResultScore