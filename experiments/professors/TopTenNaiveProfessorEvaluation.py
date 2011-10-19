from json import load
from pprint import pprint
from urllib2 import HTTPError
from src.evaluation.NaiveQueryEvaluation import NaiveQueryEvaluation
from src.search.google.GoogleSearch import GoogleSearch
from util.GoogleResultsBuilder import buildResultsFromURLs

__author__ = 'jon'

# The entities to test
entityIds = [
    'Paris Smaragdis',
    'Ralph Johnson',
    'Robin Kravets',
    'Matthew Caesar',
    'Kevin Chen-Chuan Chang',
    'Danny Dig',
    'ChengXiang Zhai'
]

# Interface with which to search google
googleSearcher = GoogleSearch()


def buildQueriesForEntity(entity):

    queries = []

    entityKey = entity['name']
    del entity['name']

    for property in entity:

        entityProperty = entity[property]

        try:
            if property is not None and property != "None":
                if type(entityProperty) == type([]):
                    for property in entityProperty:
                        queries.append('+"' + str(entityKey) + '" +"' + str(property) + '"')
                else:
                    queries.append('+"' + str(entityKey) + '" +"' + str(entityProperty) + '"')
        except:
            pass
        
    return queries


if __name__ == '__main__':

    for entityId in entityIds:

        # Get the entity object
        entity = load(open("entities/%s.json" % entityId))

        # Build the queries for this entity
        queries = buildQueriesForEntity(entity)
        queries = ["+\"%s\"" % entityId] + queries
        
        # Print the header
        title = 'Testing ' + entityId
        print
        print title
        print '=' * len(title)
        print

        # Get the ideal set of results for each query
        entityURLs = load(open("standard/%s.json" % entityId))
        idealResults = buildResultsFromURLs(entityURLs, 'src/search/google/GetPageRank.py')

        # Get the search results for each query
        queryScores = []
        totalResults = set([])
        for query in queries:

            # Get the results
            results = googleSearcher.query(query, 50, False)
            for result in results:
                totalResults.add(result['url'])

            # Evaluate this query & add the query score to the list of query scores
            queryEvaluator = NaiveQueryEvaluation(query)
            queryScore = queryEvaluator.evaluate(results, idealResults)
            queryScores.append(queryScore)

            print "%1.4f\t\t%s" % (queryScore, query)
            

        # Evaluate this query & add the query score to the list of query scores
        relevantResultsRetrieved = totalResults.intersection(set(entityURLs))
        overallScore = len(relevantResultsRetrieved) / float(len(entityURLs))

        print
        print "Overall:\t\t%1.4f" % overallScore

        print '\n'

