import os
from whoosh.analysis import StemmingAnalyzer, CharsetFilter
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.index import open_dir, create_in, exists_in
from whoosh.qparser.default import QueryParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from whoosh.support.charset import accent_map
from src.ranking.Ranking import Ranking
from src.ranking.TermFrequencyRanking import IndexRanking
from src.ranking.scorer.BM25FSpy import BM25FSpy

__author__ = 'jon'

class BM25SpyRanking(IndexRanking):
    """
      Simply exposes an interface to get scores calculated by whoosh
    """

    def __init__(self, searchResults, keywords, entityId):
        self.indexLocation = "/home/jon/.index"
        Ranking.__init__(self, searchResults, keywords)
        self.createIndex()

        
    def createIndex(self):
        """
          Build the index with the search results for this ranking
        """

        # Create the schema for the index, which stores & scores the content, title, and description
        analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)
        self.indexSchema = Schema(content=TEXT(analyzer=analyzer, stored=True), title=TEXT(analyzer=analyzer, stored=True),
                                  description=TEXT(analyzer=analyzer, stored=True), url=ID(stored=True, unique=True), pagerank=NUMERIC(stored=True),
                                  keywords=TEXT(stored=True), yqlKeywords=TEXT(stored=True), expandedYqlKeywords=TEXT(stored=True),
                                  headers=TEXT(stored=True), baselineScore=NUMERIC(stored=True))

        # Remove the index if it exists
        if not os.path.exists(self.indexLocation) or len(os.listdir(self.indexLocation)) == 0:

            if not os.path.exists(self.indexLocation):

                # Try to create the index directory
                os.mkdir(self.indexLocation)

            # Build a new index in this directory
            self.index = create_in(self.indexLocation, self.indexSchema)

        else:
            if exists_in(self.indexLocation):
                print "Opening existing index..."
                self.index = open_dir(self.indexLocation)
            else:
                raise Exception("Could not open index directory!")

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

                indexWriter.update_document(content=unicodeContent, title=unicodeTitle, description=unicodeDescription,
                                 yqlKeywords=unicodeYqlKeywords, expandedYqlKeywords=unicodeExpandedYqlKeywords,
                                 pagerank=pageRank, url=unicodeUrl, keywords=unicodeKeywords, headers=unicodeHeaders,
                                 baselineScore=baselineScore)

            except KeyError:
                pass

        # Commit all the changes, so that every change is flushed to disk, and we can safely query the index
        indexWriter.commit()



    def buildQueryParser(self):
        """
          Build the query parser that parses the specified feature
        """

        contentQueryParser = QueryParser(self.feature, schema=self.indexSchema, group=OrGroup)
        contentQueryParser.add_plugin(PlusMinusPlugin)
        return contentQueryParser


    def rank(self):

        reRankedResults = self.queryIndex(BM25FSpy)
        return reRankedResults


    def getScores(self):
        return BM25FSpy.scores

    
    def getNumerics(self):
        return BM25FSpy.numerics
