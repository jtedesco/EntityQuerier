from json import load
from pprint import pprint
from urllib2 import HTTPError
from src.evaluation.SimpleQueryEvaluator import SimpleQueryEvaluator
from src.queries.SimpleQueryBuilder import buildQueries
from src.search.google.GoogleSearch import GoogleSearch
from util.GoogleResultsBuilder import buildGoogleResultsFromURLs

__author__ = 'jon'

# The entities to test
entityIds = [
    'ChengXiang Zhai',
    'Paris Smaragdis',
    'Robin Kravets',
    'Matthew Caesar',
    'Kevin Chen-Chuan Chang',
    'Danny Dig',
    'Ralph Johnson'
]


# Interface with which to search google
googleSearcher = GoogleSearch()


if __name__ == '__main__':

    for entityId in entityIds:

        # Get the entity object
        entity = load(open("../../entities/%s.json" % entityId))

        # Build the queries for this entity
        queries = buildQueries(entity)
        queries = ["\"%s\"" % entityId] + queries
        
        # Print the header
        title = 'Testing ' + entityId
        print
        print title
        print '=' * len(title)
        print

        # Get the ideal set of results for each query
        entityURLs = load(open("../../standard/%s.json" % entityId))
        idealResults = buildGoogleResultsFromURLs(entityURLs)

        # Get the search results for each query
        queryScores = []
        totalResults = set([])
        for query in queries:

            # Get the results
            results = googleSearcher.query(query)
            for result in results:
                totalResults.add(result['url'])

            # Evaluate this query & add the query score to the list of query scores
            queryEvaluator = SimpleQueryEvaluator()
            queryScore = queryEvaluator.evaluate(results, idealResults)
            queryScores.append(queryScore)

            print "%1.4f\t\t%s" % (queryScore, query)
            

        # Evaluate this query & add the query score to the list of query scores
        relevantResultsRetrieved = totalResults.intersection(set(entityURLs))
        overallScore = len(relevantResultsRetrieved) / float(len(entityURLs))

        print
        print "Overall:\t\t%1.4f" % overallScore

        print '\n'

