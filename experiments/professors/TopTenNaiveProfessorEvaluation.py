from json import load
from pprint import pprint
from src.evaluation.NaiveQueryEvaluation import NaiveQueryEvaluation
from src.search.google.GoogleSearch import GoogleSearch
from util.GoogleResultsBuilder import buildResultsFromURLs

__author__ = 'jon'

# The entities to test
entityIds = [
    'Danny Dig',
    'ChengXiang Zhai',
    'Kevin Chen-Chuan Chang',
    'Matthew Caesar',
    'Paris Smaragdis',
    'Ralph Johnson',
    'Robin Kravets'
]

# Interface with which to search google
googleSearcher = GoogleSearch()


def buildQueriesForEntity(entity):

    queries = []

    entityKey = entity['name']
    del entity['name']

    for property in entity:

        entityProperty = entity[property]

        if property is not None:
            if type(entityProperty) == type([]):
                for property in entityProperty:
                    queries.append('+"' + str(entityKey) + '" +"' + str(property) + '"')
            else:
                queries.append('+"' + str(entityKey) + '" +"' + str(entityProperty) + '"')

    return queries


if __name__ == '__main__':

    for entityId in entityIds:

        # Get the entity object
        entity = load(open("entities/%s.json" % entityId))

        # Build the queries for this entity
        queries = buildQueriesForEntity(entity)
        
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
        for query in queries:

            try:
                # Get the results
                results = googleSearcher.query(query, 50, False)

                # Evaluate this query & add the query score to the list of query scores
                queryEvaluator = NaiveQueryEvaluation(query)
                queryScore = queryEvaluator.evaluate(results, idealResults)
                queryScores.append(queryScore)

                print  str(queryScore) + '  -  \'' + query + '\''
            except Exception:
                print 'Error running \'' + query + '\''

        print '\n'

