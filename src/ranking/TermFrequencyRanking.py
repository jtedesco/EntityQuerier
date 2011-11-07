from IN import INT_MAX
import os
import whoosh
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.index import create_in
from whoosh.qparser.default import MultifieldParser, QueryParser
from whoosh.qparser.syntax import AndGroup, Group, OrGroup
from whoosh.query import Phrase, Or
from whoosh.scoring import Frequency
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



    def createIndex(self):
        """
          Build the index with the search results for this ranking
        """

        # Create the schema for the index, which stores & scores the content, title, and description
        analyzer = StemmingAnalyzer()
        self.indexSchema = Schema(content=TEXT(analyzer=analyzer, stored=True), title=TEXT(analyzer=analyzer, stored=True),
                                  description=TEXT(analyzer=analyzer, stored=True), url=ID(stored=True), pagerank=NUMERIC(stored=True),
                                  keywords=KEYWORD(stored=True))
        indexDirectory = ".index"

        # Remove the index if it exists
        if os.path.exists(indexDirectory):
            os.rmdir(indexDirectory)

        # Try to create the index directory
        os.mkdir(indexDirectory)

        # Build a new index in this directory
        self.index = create_in(indexDirectory, self.indexSchema)

        # Get a writer for the index
        indexWriter = self.index.writer()

        # Walk the pages folder for content
        for searchResult in self.searchResults:
            try:
                unicodeContent = unicode(searchResult['content'], errors='ignore')
                unicodeTitle = unicode(searchResult['title'], errors='ignore')
                unicodeDescription = unicode(searchResult['description'], errors='ignore')
                try:
                    unicodeUrl = unicode(searchResult['url'], errors='ignore')
                except TypeError:
                    unicodeUrl = searchResult['url']
                unicodeKeywords = unicode(' '.join(searchResult['keywords']), errors='ignore')
                pageRank = searchResult['pageRank']

                if len(unicodeContent) == 0:
                    unicodeContent = u'content'
                if len(unicodeTitle) == 0:
                    unicodeTitle = u'title'
                if len(unicodeDescription) == 0:
                    unicodeDescription = u'description'
                if len(unicodeUrl) == 0:
                    unicodeUrl = u'url'
                if len(unicodeKeywords) == 0:
                    unicodeKeywords = u'keywords'

                indexWriter.add_document(content=unicodeContent, title=unicodeTitle, description=unicodeDescription,
                                     pagerank=pageRank, url=unicodeUrl, keywords=unicodeKeywords)
            except KeyError:
                pass

        # Commit all the changes, so that every change is flushed to disk, and we can safely query the index
        indexWriter.commit()


    def queryIndex(self, weightingMechanism):
        """
          Retrieve the results matching the given keywords
        """

        # Create a searcher object for this index
        searcher = self.index.searcher(weighting=weightingMechanism)

        # Create a query parser, providing it with the schema of this index, and the default field to search, 'content'
        keywordsQueryParser = QueryParser('content', schema=self.indexSchema, phraseclass=Or, group=OrGroup)
        query = ""
        for keyword in self.keywords:
            if keyword != self.entityId:
                query += "(" + self.entityId + " AND " + keyword + ") OR "
        query = query.rstrip(" OR ")
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


    def rank(self):
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(Frequency)
        return reRankedResults
