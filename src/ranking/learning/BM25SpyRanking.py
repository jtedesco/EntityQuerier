from whoosh.qparser.default import QueryParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from src.ranking.Ranking import Ranking
from src.ranking.TermFrequencyRanking import TermFrequencyRanking
from src.ranking.scorer.BM25FSpy import BM25FSpy

__author__ = 'jon'

class BM25SpyRanking(TermFrequencyRanking):
    """
      Simply exposes an interface to get scores calculated by whoosh
    """

    def __init__(self, searchResults, keywords, entityId):
        self.indexLocation = ".index-" + entityId
        Ranking.__init__(self, searchResults, keywords)
        self.createIndex()


    def buildQueryParser(self):
        """
          Build the query parser that parses the specified feature
        """

        contentQueryParser = QueryParser(self.feature, schema=self.indexSchema, group=OrGroup)
        contentQueryParser.add_plugin(PlusMinusPlugin)
        return contentQueryParser


    def rank(self):

        reRankedResults = self.queryIndex(BM25FSpy)
        return reRankedResults


    def getScores(self):
        return BM25FSpy.scores

    
    def getNumerics(self):
        return BM25FSpy.numerics
