import threading
from whoosh.analysis import StemmingAnalyzer, CharsetFilter
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.index import exists_in, open_dir
from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from whoosh.support.charset import accent_map
import thread
from src.ranking.learning.coordinateDescent.CoordinateDescentScorer import CoordinateDescentScorer
from src.util.RankingExperimentUtililty import getRankingResults

__author__ = 'jon'

class CoordinateDescentRankingThread(threading.Thread):
    """
      Thread that performs a tweak of a given feature, and reports the
    """

    def __init__(self, weights, keywords, changes, changeName, relevantResults, indexLocation):
        """
          Initializes this learning thread, by creating the index schema, analyzer, and opening the index.

            @param  keywords        Map of entity ids to keywords
            @param  weights          Weighting this thread will test
            @param  changes         Map of changes to test -> their resulting scores
            @param  changeName      Change this thread is responsible for testing
            @param  relevantResults Map of entity ids -> list of relevant urls for that entity
            @param  indexLocation   The location of the index to use
        """


        # Grab the numerical entry weighting data from the values dictionary
        self.baselineScoreWeight = weights['baselineScore']
        self.pageRankWeight = weights['pageRank']
        self.pageRankScalingWeight = weights['pageRankScaling']

        # Remove the numerical entry weighting data from the values dictionary
        del weights['baselineScore']
        del weights['pageRank']
        del weights['pageRankScaling']

        # Store the parameter data
        self.weights = weights
        self.entityIds = keywords.keys()
        self.keywords = keywords
        self.changes = changes
        self.changeName = changeName
        self.relevantResults = relevantResults

        # Create the schema for the index, which stores & scores the content, title, and description
        analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)
        self.indexSchema = Schema(content=TEXT(analyzer=analyzer, stored=True), title=TEXT(analyzer=analyzer, stored=True),
                                  description=TEXT(analyzer=analyzer, stored=True), url=ID(stored=True, unique=True), pagerank=NUMERIC(stored=True),
                                  keywords=TEXT(stored=True), yqlKeywords=TEXT(stored=True), expandedYqlKeywords=TEXT(stored=True),
                                  headers=TEXT(stored=True), baselineScore=NUMERIC(stored=True))
        threading.Thread.__init__(self)

        if exists_in(indexLocation):
            self.index = open_dir(indexLocation)
        else:
            raise Exception("Could not open index directory!")


    def buildQuery(self, entityId):

        # Create and parse the query
        query = "+\"" + entityId + "\" "
        for keyword in self.keywords[entityId]:
            if keyword != entityId:
                query += "\"" + keyword + "\" "
        query = query.rstrip()

        return query


    def buildQueryParser(self):

        # Set numerical scoring parameters
        CoordinateDescentScorer.baselineScoreWeight = self.baselineScoreWeight
        CoordinateDescentScorer.pageRankWeight = self.pageRankWeight
        CoordinateDescentScorer.pageRankScalingWeight = self.pageRankScalingWeight

        # Build parser
        keywordsQueryParser = MultifieldParser(['content','title', 'description', 'keywords', 'headers', 'yqlKeywords', 'expandedYqlKeywords'],
                                                    self.indexSchema, fieldboosts=self.weights, group=OrGroup)
        keywordsQueryParser.add_plugin(PlusMinusPlugin)
        
        return keywordsQueryParser
    

    def rank(self, entityId):
        """
          Query the index, with the provided feature weighting for the specified entity

            @param   entityId   The id of the entity for which to query
        """

        # Create a searcher object for this index
        searcher = self.index.searcher(weighting=CoordinateDescentScorer)

        # Create a query parser, build the query & parse it
        keywordsQueryParser = self.buildQueryParser()
        query = self.buildQuery(entityId)
        queryObject = keywordsQueryParser.parse(query)

        # Perform the query itself
        searchResults = searcher.search(queryObject, 200)

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
                'baselineScore': searchResult['baselineScore'],
                'pageRank': searchResult['pagerank']
            }
            results.append(result)

        # Return the list of web pages along with the terms used in the search
        return results


    def evaluateResults(self, results, relevantResults):
        """
          Returns a score based on the results, specifically computing recall, precision, and avg precision
        """

        recallAt1, recallAt10, recallAt20, recallAt50, precisionAt1, precisionAt10, precisionAt20, precisionAt50, \
            averagePrecisionAt1, averagePrecisionAt10, averagePrecisionAt20, averagePrecisionAt50, rPrecision, fullPrecision = getRankingResults(results, relevantResults, 200)
        
        return averagePrecisionAt1 + averagePrecisionAt10 + averagePrecisionAt20 + averagePrecisionAt50


    def run(self):

        # Accumulates the average score for this feature change for this entity
        averageResultScore = 0

        # Collect the results on this thread
        self.results = {}

        print "starting thread"
        for entityId in self.entityIds:

            # Rank results for this entity, and tally the score
            self.results[entityId] = self.rank(entityId)
            resultsScore = self.evaluateResults(self.results[entityId], self.relevantResults[entityId])

            averageResultScore += resultsScore

        averageResultScore /= len(self.entityIds)

        # Record this score in the change map
        self.changes['lock'].acquire()
        self.changes[self.changeName] = averageResultScore
        self.changes['lock'].release()

        print "Finished running thread"
