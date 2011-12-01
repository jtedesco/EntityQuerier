from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from src.ranking.BM25Ranking import BM25Ranking

__author__ = 'jon'

class BM25HeadersRanking(BM25Ranking):
    """
      Ranking that equally weights content and page header text
    """

    def buildQueryParser(self):

        headersQueryParser = MultifieldParser(['content', 'headers'], schema=self.indexSchema, group=OrGroup)
        headersQueryParser.add_plugin(PlusMinusPlugin)

        return headersQueryParser