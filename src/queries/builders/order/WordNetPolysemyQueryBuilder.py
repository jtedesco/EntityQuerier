from pprint import pprint
import subprocess
from src.queries.builders.QueryBuilder import QueryBuilder
from src.queries.builders.operator.AttributeNamesQueryBuilder import AttributeNamesQueryBuilder
from src.queries.builders.operator.AttributeValuesQueryBuilder import AttributeValuesQueryBuilder

__author__ = 'jon'


class WordNetPolysemyQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity, using both names and values of schema
    """

    def __init__(self):

        self.entityNamesQueryBuilder = AttributeNamesQueryBuilder()
        self.entityValuesQueryBuilder = AttributeValuesQueryBuilder()


    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        # Get the lists of name & value queries
        nameQueries = self.entityNamesQueryBuilder.buildQueries(entity, idField)
        idQuery = nameQueries[0]
        nameQueries = nameQueries[1:]
        valueQueries = self.entityValuesQueryBuilder.buildQueries(entity, idField)[1:]

        # The final list of queries
        queries = nameQueries + valueQueries
        queries.remove(idQuery + ' ' + idQuery)

        # Put all queries to lower case
        for index in xrange(0, len(queries)):
            queries[index] = queries[index].lower()
        queries = list(set(queries))

        # For each query, build the sum of polysemy of each word
        queryScores = []
        for query in queries:
            polysemyScore = self.scoreQuery(query)
            queryScores.append(polysemyScore)

        # Get the list of queries sorted by their scores in reverse
        queriesAndScores = zip(queryScores, queries)
        queriesAndScores.sort(reverse=True)
        scores, queries = zip(*queriesAndScores)

        # Add the id query
        queries = list(queries)
        queries.insert(0, idQuery)

        # Let's just take the first 10 queries
        return queries[0:11]

    
    def scoreQuery(self, query):
        """
          Score query by getting the sum of polysemy count of words in the query (we're going to assume that words that
            WordNet doesn't recognize are very useful, and assume there are no spelling errors).
        """

        # The template WordNet command
        wordNetArgumentTemplate = "%s -famln -famlr -famla -famlv"

        score = 0
        for keyword in query.split():
            
            # Call WordNet & get output
            arguments = (wordNetArgumentTemplate % keyword).split()
            p = subprocess.Popen(['wn'] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, errors = p.communicate()

            # Parse output
            if len(output) == 0:
                score += 15
            else:
                for line in output.split('\n'):
                    if 'polysemy count' in line:
                        countIndex = line.find('polysemy count') + len('polysemy count = ')
                        scoreString = line[countIndex:].rstrip(')')
                        score += int(scoreString)

        return score
        
        
