import threading
from experiments.RankingExperiment import RankingExperiment
from experiments.retrieval.EntityAttributeValues import EntityAttributeValues
from src.queries.EntityAttributeValuesQueryBuilder import ExactAttributeValuesQueryBuilder
from src.search.extension.BaselineScoreExtension import BaselineScoreExtension
from src.search.extension.ExpandedYQLKeywordExtension import ExpandedYQLKeywordExtension
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class SearchThread(threading.Thread):

    
    def __init__(self, dictionary):
        """
          Initialize this parser, given the dictionary into which the page's data is going to be placed
        """
        threading.Thread.__init__(self)

        # Pull the data out of the dictionary
        self.dictionary = dictionary
        self.entity = dictionary['entity']
        self.entityId = dictionary['entityId']
        self.trigger = dictionary['trigger']

        
    def update(self, message):
        """
          Updates the UI saying with the given message
        """

        self.dictionary['status'] = message
        self.trigger.release()

        
    def run(self):
        """
          Run the search, and update the dictionary (releasing the lock to trigger a callback whenever one should occur)
        """

        # Run retrieval phase
        self.update("Running retrieval phase")
        numberOfSearchResults = 50
        searchInterface = GoogleSearch(numberOfSearchResults, True, [])
        experiment = EntityAttributeValues([self.entityId], searchInterface, ExactAttributeValuesQueryBuilder(), numberOfSearchResults)
        experiment.run()
        temporaryFileName = "tmp-output" + self.entityId
        experiment.printResults(temporaryFileName)

        # Run ranking phase
        self.update("Running ranking phase")
        extensions = [
            PageRankExtension(),
            YQLKeywordExtension(),
            ExpandedYQLKeywordExtension(),
            BaselineScoreExtension()
        ]
        rankingExperiment = RankingExperiment(temporaryFileName, self.entity, experiment, extensions, True, True)
        results = rankingExperiment.rank()
        self.dictionary['results'] = results

        # Signal that we're finally done
        self.update("done")

