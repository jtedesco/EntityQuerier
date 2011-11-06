import operator
import os
from pprint import pprint
import re
from whoosh import scoring
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, exists_in
from whoosh.qparser.default import QueryParser
from whoosh.qparser.syntax import OrGroup
from whoosh.query import Or
import sys
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
        self.indexSchema = Schema(content=TEXT(stored=True), title=TEXT(stored=True), description=TEXT(stored=True), url=TEXT(stored=True))
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
                    
                indexWriter.add_document(content=unicodeContent, title=unicodeTitle,
                                     description=unicodeDescription, url=unicodeUrl)
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
        queryParser = QueryParser('content', schema=self.indexSchema, phraseclass=Or, group=OrGroup)
        query = ' '.join(self.keywords)
        queryObject = queryParser.parse(query)

        # Perform the query itself
        searchResults = searcher.search(queryObject, 1000)

        # Format the results
        results = []
        for searchResult in searchResults:

            result = {
                'url': searchResult['url'],
                'content': searchResult['content'],
                'title': searchResult['title'],
                'description': searchResult['description']
            }
            results.append(result)

        # Return the list of web pages along with the terms used in the search
        return results
    

    def rank(self):
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(scoring.Frequency)
        return reRankedResults
        