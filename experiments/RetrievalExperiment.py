from json import load, dumps
import os
from src.evaluation.CompositeQueryEvaluator import CompositeQueryEvaluator

__author__ = 'jon'

class RetrievalExperiment(object):
    """
      A generic experiment to be run
    """

    def __init__(self, entityIds, searchInterface, queryBuilder, numberOfResults=50):
        """
          Put the search interface and entity ids on this object, and load entity data
        """

        # The list of ids (corresponding JSON files are expected to be found in 'standard' and 'entities' folders)
        self.entityIds = entityIds

        # The search framework to use
        self.searchInterface = searchInterface
        self.numberOfResults = numberOfResults

        # The query evaluation metric to use
        self.queryEvaluator = CompositeQueryEvaluator()

        # The query builder to use
        self.queryBuilder = queryBuilder

        # Build the entities and queries for these entities
        self.buildEntities()
        self.buildQueries()

        # Build the 'golden standard', the ideal set of documents to be retrieved
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

            # Find the project root & open the input entity
            projectRoot = str(os.getcwd())
            projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

            # Get the entity object
            entity = load(open(projectRoot + '/entities/%s.json' % entityId))
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

            # Find the project root & open the input entity
            projectRoot = str(os.getcwd())
            projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]


            idealURLs = load(open(projectRoot + "/standard/%s.json" % entityId))
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
            self.results[entityId] = {}

        for entityId in self.entityIds:

            # The URLs retrieved using all the queries for this entity
            totalURLs = set([])
            otherPrecisions = []
            for query in self.queries[entityId]:

                queryURLs = []

                # Run this query
                queryResults = self.searchInterface.query(query, False)

                # Add the retrieved results
                if queryResults is not None:
                    for result in queryResults:

                        # Add the new URL to our lists of URLs retrieved
                        try:
                            resultURL = str(result['url']).strip()
                            totalURLs.add(resultURL)
                            queryURLs.append(resultURL)
                        except TypeError:
                            print "Something went very wrong..."
                        except UnicodeDecodeError:
                            pass
                        except UnicodeEncodeError:
                            pass

                # Score this query
                queryScore = self.queryEvaluator.evaluate(queryURLs, self.idealURLs[entityId])

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
                try:
                    otherPrecisions.append(queryScore['precision'])
                except Exception:
                    pass

                # Score the query & gather results
                for url in queryURLs:

                    # Update lists of relevant results
                    if url in self.idealURLs[entityId]:
                        self.results[entityId][query]['relevantDocumentsRetrieved'].append(url)
                    else:
                        self.results[entityId][query]['nonRelevantDocumentsRetrieved'].append(url)


            # Score the set of queries
            try:
                queryScore = self.queryEvaluator.evaluate(totalURLs, self.idealURLs[entityId], otherPrecisions)
            except Exception:
                queryScore = self.queryEvaluator.evaluate(totalURLs, self.idealURLs[entityId])

            # Get list of relevant documents not retrieved
            relevantDocumentsNotRetrieved = list(set(self.idealURLs[entityId]).difference(set(totalURLs)))

            # Allocate space in the new results data structure
            self.results[entityId]['overall'] = {
                'documentsRetrieved' : list(totalURLs),
                'relevantDocumentsRetrieved' : [],
                'nonRelevantDocumentsRetrieved' : [],
                'relevantDocumentsNotRetrieved' : relevantDocumentsNotRetrieved,
                'score' : queryScore
            }

            # Score the query & gather results
            for url in totalURLs:

                # Update lists of relevant results
                if url in self.idealURLs[entityId]:
                    self.results[entityId]['overall']['relevantDocumentsRetrieved'].append(url)
                else:
                    self.results[entityId]['overall']['nonRelevantDocumentsRetrieved'].append(url)

        return self.results

                    
    def printResults(self, outputPath = "output", entityId = None):

        # Summarize the results\
        summaryOutput = "Results Summary\n"
        summaryOutput += "===============\n\n"
        summaryOutput += '\t' + entityId + ":\n"
        summaryOutput += '\t' + len(entityId) * '~' + '\n'
        for metric in self.results[entityId]['overall']['score']:
            summaryOutput += '\t' + metric.title() + ": %1.5f\n" % self.results[entityId]['overall']['score'][metric]
        summaryOutput += '\t' + (len(entityId) * '~') + '\n'
        summaryOutput += '\n'

        # Format the results
        resultsOutput = dumps(self.results, indent=4)

        # Write it out
        if os.path.exists(outputPath):
            os.remove(outputPath)
        outputFile = open(outputPath, 'w')
        outputFile.write(summaryOutput)
        outputFile.write(resultsOutput)
        outputFile.close()

            