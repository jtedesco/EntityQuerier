from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from src.ranking.BM25Ranking import BM25Ranking

__author__ = 'jon'

class BM25YahooKeywordsRanking(BM25Ranking):
    """
      Ranking that equally scores the content and the Yahoo keywords
    """

    def buildQueryParser(self):

        yahooKeywordsQueryParser = MultifieldParser(['content', 'yqlKeywords'], schema=self.indexSchema, group=OrGroup)
        yahooKeywordsQueryParser.add_plugin(PlusMinusPlugin)

        return yahooKeywordsQueryParser
