import os
from whoosh import scoring
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.index import create_in
from whoosh.qparser.default import QueryParser, MultifieldParser
from whoosh.qparser.syntax import OrGroup
from whoosh.query import Or
from src.ranking.TFIDFRanking import TermFrequencyRanking
from src.ranking.TermVectorRanking import TermVectorRanking

__author__ = 'jon'

class BM25Ranking(TermFrequencyRanking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def rank(self):
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(scoring.BM25F)
        return reRankedResults
