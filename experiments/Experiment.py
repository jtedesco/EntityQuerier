from json import load
from pprint import pprint

__author__ = 'jon'

class Experiment(object):
    """
      A generic experiment to be run
    """

    def __init__(self, entityIds, searchInterface):
        """
          Put the search interface and entity ids on this object, and load entity data
        """

        self.entityIds = entityIds
        self.searchInterface = searchInterface

        self.buildEntities()
        self.buildIdealResultURLs()


    def buildQueries(self):
        """
          Builds the queries to use for each entity
        """

        # Build the queries for this entity
        self.queries = {}
        for entityId in self.entityIds:
            self.queries[entityId] = self.queryBuilder.buildQueries(self.entities[entityId])


    def buildEntities(self):
        """
          Load entity data into this object
        """

        # Build the list of entities and queries to be used
        self.entities = {}
        for entityId in self.entityIds:

            # Get the entity object
            entity = load(open("../../entities/%s.json" % entityId))
            self.entities[entityId] = entity


    def buildIdealResultURLs(self):
        """
          Builds the ideal list of retrieved URLs, and the corresponding results.

          Data structure created will be:

            self.idealURLs = {
                <entity id> : [
                    <url>
                    <url>
                    ...
                ]
            }

        """

        self.idealURLs = {}
        for entityId in self.entityIds:
            idealURLs = load(open("../../standard/%s.json" % entityId))
            self.idealURLs[entityId] = set(idealURLs)

            
    def run(self):
        """
          Actually runs the experiment.

          Creates results on this object, structured like this:

            self.results = {
                <entity id> :
                    <query> : {
                        relevantDocumentsRetrieved : [
                            ...
                        ]
                        nonRelevantDocumentsRetrieved : [
                            ...
                        ]
                        relevantDocumentsNotRetrieved : [
                            ...
                        ]
                        nonRelevantDocumentsNotRetrieved : [
                            ...
                        ]
                        score : <query score>
                    }

                    ... (same thing for all queries) ...

                    overall : {
                        relevantDocumentsRetrieved : [
                            ...
                        ]
                        nonRelevantDocumentsRetrieved : [
                            ...
                        ]
                        relevantDocumentsNotRetrieved : [
                            ...
                        ]
                        nonRelevantDocumentsNotRetrieved : [
                            ...
                        ]
                        score : <query score>
                    }
                ...
            }

            Where each entry not specified will be 
        """

        # The final results data
        self.results = {}

        for entityId in self.entityIds:

            # The URLs retrieved using all the queries for this entity
            totalURLs = set([])
            for query in self.queries[entityId]:

                queryURLs = []

                # Run this query
                queryResults = self.searchInterface.query(query)

                # Add the retrieved results
                for result in queryResults:

                    # Add the new URL to our lists of URLs retrieved
                    resultURL = result['url']
                    totalURLs.add(resultURL)
                    queryURLs.append(resultURL)

                # Score this query
                queryScore = self.queryEvaluator.evalute(queryURLs, self.idealURLs[entityId])

                # Get list of relevant documents not retrieved
                relevantDocumentsNotRetrieved = list(set(self.idealURLs[entityId]).difference(set(queryURLs)))

                # Allocate space in the new results data structure
                self.results[entityId][query] = {
                    'documentsRetrieved' : queryURLs,
                    'relevantDocumentsRetrieved' : [],
                    'nonRelevantDocumentsRetrieved' : [],
                    'relevantDocumentsNotRetrieved' : relevantDocumentsNotRetrieved,
                    'score' : queryScore
                }

                # Score the query & gather results
                for url in queryURLs:

                    # Update lists of relevant results
                    if url in self.idealURLs[entityId]:
                        self.results[entityId][query]['relevantDocumentsRetrieved'].append(url)
                    else:
                        self.results[entityId][query]['nonRelevantDocumentsRetrieved'].append(url)


            # Score the set of queries
            queryScore = self.queryEvaluator.evalute(totalURLs, self.idealURLs[entityId])

            # Get list of relevant documents not retrieved
            relevantDocumentsNotRetrieved = list(set(self.idealURLs[entityId]).difference(set(totalURLs)))

            # Allocate space in the new results data structure
            self.results[entityId]['overall'] = {
                'documentsRetrieved' : totalURLs,
                'relevantDocumentsRetrieved' : [],
                'nonRelevantDocumentsRetrieved' : [],
                'relevantDocumentsNotRetrieved' : relevantDocumentsNotRetrieved,
                'score' : queryScore
            }

            # Score the query & gather results
            for url in totalURLs:

                # Update lists of relevant results
                if url in self.idealURLs[entityId]:
                    self.results[entityId][query]['relevantDocumentsRetrieved'].append(url)
                else:
                    self.results[entityId][query]['nonRelevantDocumentsRetrieved'].append(url)


    def printResults(self):
        pprint(self.results)
            