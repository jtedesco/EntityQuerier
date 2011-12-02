from IN import INT_MAX
import os
import whoosh
from whoosh.analysis import StemmingAnalyzer, CharsetFilter
from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.index import create_in, exists_in, open_dir
from whoosh.qparser.default import QueryParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from whoosh.scoring import Frequency
from whoosh.support.charset import accent_map
import sys
from src.ranking.TermVectorRanking import TermVectorRanking

__author__ = 'jon'

class TermFrequencyRanking(TermVectorRanking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def __init__(self, searchResults, keywords):
        self.indexLocation = ".index"
        TermVectorRanking.__init__(self, searchResults, keywords)
        self.createIndex()

        
    @staticmethod
    def getIndexLocation():
        return ".index"


    def createIndex(self):
        """
          Build the index with the search results for this ranking
        """

        # Create the schema for the index, which stores & scores the content, title, and description
        analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)
        self.indexSchema = Schema(content=TEXT(analyzer=analyzer, stored=True), title=TEXT(analyzer=analyzer, stored=True),
                                  description=TEXT(analyzer=analyzer, stored=True), url=ID(stored=True), pagerank=NUMERIC(stored=True),
                                  keywords=TEXT(stored=True), yqlKeywords=TEXT(stored=True), expandedYqlKeywords=TEXT(stored=True),
                                  headers=TEXT(stored=True), baselineScore=NUMERIC(stored=True))

        # Remove the index if it exists
        if not os.path.exists(self.indexLocation):

            # Try to create the index directory
            os.mkdir(self.indexLocation)

            # Build a new index in this directory
            self.index = create_in(self.indexLocation, self.indexSchema)

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
                    except KeyError:
                        unicodeYqlKeywords = u''

                    try:
                        unicodeExpandedYqlKeywords = unicode(', '.join(searchResult['expandedYqlKeywords']), errors='ignore')
                    except TypeError:
                        unicodeExpandedYqlKeywords = ', '.join(searchResult['expandedYqlKeywords'])
                    except KeyError:
                        unicodeExpandedYqlKeywords = u''

                    try:
                        unicodeHeaders = unicode(', '.join(searchResult['headers']), errors='ignore')
                    except TypeError:
                        unicodeHeaders = ', '.join(searchResult['headers'])
                    except KeyError:
                        unicodeHeaders = u''

                    try:
                        pageRank = searchResult['pageRank']
                    except KeyError:
                        pageRank = 0

                    try:
                        baselineScore = searchResult['baselineScore']
                    except KeyError:
                        baselineScore = 0


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
                    if len(unicodeExpandedYqlKeywords) == 0:
                        unicodeExpandedYqlKeywords = u'?'
                    if len(unicodeHeaders) == 0:
                        unicodeHeaders = u'?'

                    indexWriter.add_document(content=unicodeContent, title=unicodeTitle, description=unicodeDescription,
                                     yqlKeywords=unicodeYqlKeywords, expandedYqlKeywords=unicodeExpandedYqlKeywords,
                                     pagerank=pageRank, url=unicodeUrl, keywords=unicodeKeywords, headers=unicodeHeaders,
                                     baselineScore=baselineScore)

                except KeyError:
                    pass

            # Commit all the changes, so that every change is flushed to disk, and we can safely query the index
            indexWriter.commit()

        else:
            if exists_in(self.indexLocation):
                print "Opening existing index..."
                self.index = open_dir(self.indexLocation)
            else:
                raise Exception("Could not open index directory!")


    def buildQueryParser(self):
        """
          Build the query parser
        """

        contentQueryParser = QueryParser('content', schema=self.indexSchema, group=OrGroup)
        contentQueryParser.add_plugin(PlusMinusPlugin)
        return contentQueryParser


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
    

    def queryIndex(self, weightingMechanism):
        """
          Retrieve the results matching the given keywords
        """

        # Create a searcher object for this index
        searcher = self.index.searcher(weighting=weightingMechanism)

        # Create a query parser, providing it with the schema of this index, and the default field to search, 'content'
        keywordsQueryParser = self.buildQueryParser()
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


    def rank(self):
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(Frequency)
        return reRankedResults
