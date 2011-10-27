from src.queries.EntityAttributeNamesQueryBuilder import EntityAttributeNamesQueryBuilder
from src.queries.EntityAttributeValuesQueryBuilder import EntityAttributeValuesQueryBuilder
from src.queries.QueryBuilder import QueryBuilder

__author__ = 'jon'


class EntityAttributeNamesAndValuesQueryWithOperatorsBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity, using both names and values of schema
    """

    def __init__(self):

        self.entityNamesQueryBuilder = EntityAttributeNamesQueryBuilder()
        self.entityValuesQueryBuilder = EntityAttributeValuesQueryBuilder()


    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, using query operators.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        # Get the basic name & values queries
        oldQueries = []
        nameQueries = self.entityNamesQueryBuilder.buildQueries(entity, idField)
        valueQueries = self.entityValuesQueryBuilder.buildQueries(entity, idField)
        oldQueries.extend(nameQueries)
        oldQueries.extend(valueQueries)

        # Add '+' operators to the queries
        queries = []
        for basicQuery in oldQueries:

            newQuery = '+' + str(basicQuery)
            newQuery = newQuery.replace(' "', ' +"')

            queries.append(newQuery)

        return queries
