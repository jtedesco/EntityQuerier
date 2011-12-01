from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from src.ranking.BM25Ranking import BM25Ranking

__author__ = 'jon'

class BM25DescriptionRanking(BM25Ranking):
    """
      Ranking that scores both content and meta description equally
    """

    def buildQueryParser(self):

        descriptionQueryParser = MultifieldParser(['content', 'description'], schema=self.indexSchema, group=OrGroup)
        descriptionQueryParser.add_plugin(PlusMinusPlugin)
        
        return descriptionQueryParser
