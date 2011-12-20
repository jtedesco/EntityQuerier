from src.ranking.BM25Ranking import BM25Ranking
from src.util.ResultsBuilderUtility import getResultsFromRetrievalFile
from src.util.Utility import getKeywords

__author__ = 'jon'


class RankingExperiment(object):
    """
      Rank search results
    """

    def __init__(self, resultsFilePath, entity, rankingScheme = BM25Ranking, extensions = [], includeOriginalResults = False, verbose = False, fetchResults = True):

        if fetchResults:

            self.results = getResultsFromRetrievalFile(resultsFilePath, extensions)
            print "Retrieved all results from web!"

        else:
            self.results = []
            self.resultsDump = []

        # Get the keywords & build the ranking scheme
        keywords = getKeywords(entity)
        if includeOriginalResults:
            self.rankingScheme = rankingScheme(self.results, keywords, self.resultsDump)
        else:
            self.rankingScheme = rankingScheme(self.results, keywords)
        self.rankingScheme.entity = entity
        self.rankingScheme.entityId = entity['name']

        
    def rank(self):
        """
          Get the ranked results using this ranking scheme
        """
        return self.rankingScheme.rank()
