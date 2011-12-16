from IN import INT_MAX
import whoosh
from whoosh.analysis import StemmingAnalyzer, CharsetFilter
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.index import open_dir, exists_in
from whoosh.qparser.default import QueryParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from whoosh.support.charset import accent_map
from src.ranking.scorer.BM25FSpy import BM25FSpy

__author__ = 'jon'

class BM25SpyRanking(object):
    """
      Simply exposes an interface to get scores calculated by whoosh
    """

    @staticmethod
    def getIndexLocation():
        return "/home/jon/Documents/.index"


    def __init__(self, keywords, entityId):

        self.indexLocation = BM25SpyRanking.getIndexLocation()

        self.keywords = keywords
        self.entityId = entityId

        self.openIndex()

        
    def openIndex(self):
        """
          Opens the index
        """

        # Create the schema for the index, which stores & scores the content, title, and description
        analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)
        self.indexSchema = Schema(content=TEXT(analyzer=analyzer, stored=True), title=TEXT(analyzer=analyzer, stored=True),
                                  description=TEXT(analyzer=analyzer, stored=True), url=ID(stored=True, unique=True), pagerank=NUMERIC(stored=True),
                                  keywords=TEXT(stored=True), yqlKeywords=TEXT(stored=True), expandedYqlKeywords=TEXT(stored=True),
                                  headers=TEXT(stored=True), baselineScore=NUMERIC(stored=True))

        # Remove the index if it exists
        if exists_in(self.indexLocation):
            print "Opening existing index..."
            self.index = open_dir(self.indexLocation)
        else:
            raise Exception("Could not open index directory!")
        

    def buildQuery(self):
        """
          Builds the query for Whoosh
        """

        query = "+\"" + self.entityId + "\" "
        for keyword in self.keywords:
            if keyword != self.entityId:
                query += "\"" + keyword + "\" "
        query = query.rstrip()

        return query
    

    def queryIndex(self, weightingMechanism, feature):
        """
          Retrieve the results matching the given keywords
        """

        # Create a searcher object for this index
        searcher = self.index.searcher(weighting=weightingMechanism)

        # Create a query parser, providing it with the schema of this index, and the default field to search, 'content'
        keywordsQueryParser = self.buildQueryParser(feature)
        query = self.buildQuery()
        queryObject = keywordsQueryParser.parse(query)

        # Perform the query itself
        try:
            searchResults = searcher.search(queryObject, INT_MAX)
        except whoosh.reading.TermNotFound:
            print "Term not found!"
            searchResults = []

        # Format the results
        results = []
        for searchResult in searchResults:

            result = {
                'url': searchResult['url'],
                'content': searchResult['content'],
                'title': searchResult['title'],
                'description': searchResult['description'],
                'keywords': searchResult['keywords'],
                'headers': searchResult['headers'],
                'yqlKeywords': searchResult['yqlKeywords'],
                'expandedYqlKeywords': searchResult['expandedYqlKeywords'],
                'pageRank': searchResult['pagerank'],
                'baselineScore': searchResult['baselineScore']
            }
            results.append(result)

        # Return the list of web pages along with the terms used in the search
        return results


    def buildQueryParser(self, feature):
        """
          Build the query parser that parses the specified feature

            @param  feature     The feature on which this ranking will be based
        """

        contentQueryParser = QueryParser(feature, schema=self.indexSchema, group=OrGroup)
        contentQueryParser.add_plugin(PlusMinusPlugin)
        return contentQueryParser


    def rank(self, feature):
        """
          Rank by a given feature

            @param  feature     The feature on which this ranking will be based
        """

        reRankedResults = self.queryIndex(BM25FSpy, feature)
        return reRankedResults


    def getScores(self):
        return BM25FSpy.scores

    
    def getNumerics(self):
        return BM25FSpy.numerics
