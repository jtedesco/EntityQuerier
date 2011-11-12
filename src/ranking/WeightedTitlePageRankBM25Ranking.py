from IN import INT_MAX
import whoosh
from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import Plugin, PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from whoosh.query import Or
from src.ranking.BM25Ranking import BM25Ranking

__author__ = 'jon'

class WeightedTitlePageRankBM25Ranking(BM25Ranking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """


    def __init__(self, searchResults, keywords, titleWeight=5.0):
        """
          Creates a ranking object with the necessary parameters

            @param  searchResults   The list of search results, in the following format:
                                        [
                                            {
                                                'url': <url>
                                                'preview' : <preview snippet>
                                                'title' : <title>
                                                'description' : <meta description>
                                                'pageRank' : <PageRank, between 0 and 10>
                                                'content' : <page content>
                                            },
                                            ...
                                        ]
            @param  keywords        The keywords for these search results to use for scoring the results
            @param  titleWeight     The boost factor to be applied to the title field for ranking (no boost is 1.0)
        """
        BM25Ranking.__init__(self, searchResults, keywords)
        self.titleWeight = titleWeight

    def getIndexLocation(self):
        indexLocation = ".index-bm25-pr-weightedtitle"
        return indexLocation


    def queryIndex(self, weightingMechanism):
        """
          Retrieve the results matching the given keywords
        """

        # Create a searcher object for this index
        searcher = self.index.searcher(weighting=weightingMechanism)

        # Create a query parser, providing it with the schema of this index, and the default field to search, 'content'
        termBoosts = {
            'title' : self.titleWeight,
            'content' : 1.0
        }
        keywordsQueryParser = MultifieldParser(['title', 'content'], self.indexSchema, fieldboosts=termBoosts, group=OrGroup)
        keywordsQueryParser.add_plugin(PlusMinusPlugin)
        query = "+\"" + self.entityId + "\" "
        for keyword in self.keywords:
            if keyword != self.entityId:
                query += "\"" + keyword + "\" "
        query = query.rstrip()
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
                'pageRank': searchResult['pagerank']
            }
            results.append(result)

        # Return the list of web pages along with the terms used in the search
        return results