from IN import INT_MAX
import os
from pprint import pprint
import whoosh
from whoosh.analysis import StemmingAnalyzer, CharsetFilter
from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.index import create_in, exists_in, open_dir
from whoosh.qparser.default import QueryParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from whoosh.scoring import Frequency
from whoosh.support.charset import accent_map
from src.ranking.TermVectorRanking import TermVectorRanking

__author__ = 'jon'

class TermFrequencyRanking(TermVectorRanking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """


    def __init__(self, searchResults, keywords):
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
        """
        TermVectorRanking.__init__(self, searchResults, keywords)

        self.createIndex()


    def getIndexLocation(self):
        indexDirectory = ".index"
        return indexDirectory


    def createIndex(self):
        """
          Build the index with the search results for this ranking
        """

        # Create the schema for the index, which stores & scores the content, title, and description
        analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)
        self.indexSchema = Schema(content=TEXT(analyzer=analyzer, stored=True), title=TEXT(analyzer=analyzer, stored=True),
                                  description=TEXT(analyzer=analyzer, stored=True), url=ID(stored=True), pagerank=NUMERIC(stored=True),
                                  keywords=TEXT(stored=True), yqlKeywords=TEXT(stored=True), headers=TEXT(stored=True))
        indexDirectory = self.getIndexLocation()

        # Remove the index if it exists
        if not os.path.exists(indexDirectory):

            # Try to create the index directory
            os.mkdir(indexDirectory)

            # Build a new index in this directory
            self.index = create_in(indexDirectory, self.indexSchema)

            # Get a writer for the index
            indexWriter = self.index.writer()

            # Walk the pages folder for content
            for searchResult in self.searchResults:

                try:
                    try:
                        unicodeContent = unicode(searchResult['content'], errors='ignore')
                    except TypeError:
                        unicodeContent = searchResult['content']
                    try:
                        unicodeTitle = unicode(searchResult['title'], errors='ignore')
                    except TypeError:
                        unicodeTitle = searchResult['title']
                    try:
                        unicodeDescription = unicode(searchResult['description'], errors='ignore')
                    except TypeError:
                        unicodeDescription = searchResult['description']
                    try:
                        unicodeUrl = unicode(searchResult['url'], errors='ignore')
                    except TypeError:
                        unicodeUrl = searchResult['url']
                    try:
                        unicodeKeywords = unicode(', '.join(searchResult['keywords']), errors='ignore')
                    except TypeError:
                        unicodeKeywords = ', '.join(searchResult['keywords'])
                    try:
                        unicodeYqlKeywords = unicode(', '.join(searchResult['yqlKeywords']), errors='ignore')
                    except TypeError:
                        unicodeYqlKeywords = ', '.join(searchResult['yqlKeywords'])
                    try:
                        unicodeHeaders = unicode(', '.join(searchResult['headers']), errors='ignore')
                    except TypeError:
                        unicodeHeaders = ', '.join(searchResult['headers'])

                    pageRank = searchResult['pageRank']

                    if len(unicodeContent) == 0:
                        unicodeContent = u'?'
                    if len(unicodeTitle) == 0:
                        unicodeTitle = u'?'
                    if len(unicodeDescription) == 0:
                        unicodeDescription = u'?'
                    if len(unicodeUrl) == 0:
                        unicodeUrl = u'?'
                    if len(unicodeKeywords) == 0:
                        unicodeKeywords = u'?'
                    if len(unicodeYqlKeywords) == 0:
                        unicodeYqlKeywords = u'?'
                    if len(unicodeHeaders) == 0:
                        unicodeHeaders = u'?'

                    indexWriter.add_document(content=unicodeContent, title=unicodeTitle, description=unicodeDescription, yqlKeywords=unicodeYqlKeywords,
                                         pagerank=pageRank, url=unicodeUrl, keywords=unicodeKeywords, headers=unicodeHeaders)

                except KeyError:
                    pass

            # Commit all the changes, so that every change is flushed to disk, and we can safely query the index
            indexWriter.commit()

        else:
            if exists_in(indexDirectory):
                self.index = open_dir(indexDirectory)
            else:
                raise Exception("Could not open index directory!")


    def queryIndex(self, weightingMechanism):
        """
          Retrieve the results matching the given keywords
        """

        # Create a searcher object for this index
        searcher = self.index.searcher(weighting=weightingMechanism)

        # Create a query parser, providing it with the schema of this index, and the default field to search, 'content'
        keywordsQueryParser = QueryParser('content', schema=self.indexSchema, group=OrGroup)
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
                'headers': searchResult['headers'],
                'yqlKeywords': searchResult['yqlKeywords'],
                'pageRank': searchResult['pagerank']
            }
            results.append(result)

        # Return the list of web pages along with the terms used in the search
        return results


    def rank(self):
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(Frequency)
        return reRankedResults
