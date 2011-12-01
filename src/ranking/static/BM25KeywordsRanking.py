from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from src.ranking.BM25Ranking import BM25Ranking

__author__ = 'jon'

class BM25KeywordsRanking(BM25Ranking):
    """
      Ranking that equally weights content and meta keywords
    """

    def buildQueryParser(self):

        keywordsQueryParser = MultifieldParser(['content', 'keywords'], schema=self.indexSchema, group=OrGroup)
        keywordsQueryParser.add_plugin(PlusMinusPlugin)

        return keywordsQueryParser
