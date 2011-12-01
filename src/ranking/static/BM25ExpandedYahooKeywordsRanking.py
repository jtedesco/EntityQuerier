from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from src.ranking.BM25Ranking import BM25Ranking

__author__ = 'jon'

class BM25ExpandedYahooKeywordsRanking(BM25Ranking):
    """
      Ranking that equally weights content and expanded Yahoo keywords
    """

    def buildQueryParser(self):

        expandedYahooKeywordsQueryParser = MultifieldParser(['content', 'expandedYqlKeywords'], schema=self.indexSchema, group=OrGroup)
        expandedYahooKeywordsQueryParser.add_plugin(PlusMinusPlugin)

        return expandedYahooKeywordsQueryParser
