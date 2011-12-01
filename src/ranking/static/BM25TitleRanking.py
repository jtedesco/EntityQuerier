from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from src.ranking.BM25Ranking import BM25Ranking

__author__ = 'jon'

class BM25TitleRanking(BM25Ranking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def buildQueryParser(self):

        titleQueryParser = MultifieldParser(['content', 'title'], schema=self.indexSchema, group=OrGroup)
        titleQueryParser.add_plugin(PlusMinusPlugin)

        return titleQueryParser
