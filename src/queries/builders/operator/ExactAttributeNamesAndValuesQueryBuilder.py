from src.queries.ExactAttributeNamesQueryBuilder import ExactAttributeNamesQueryBuilder
from src.queries.ExactAttributeValuesQueryBuilder import ExactAttributeValuesQueryBuilder
from src.queries.QueryBuilder import QueryBuilder

__author__ = 'jon'


class ExactAttributeNamesAndValuesQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity, using both names and values of schema
    """

    def __init__(self):

        self.entityNamesQueryBuilder = ExactAttributeNamesQueryBuilder()
        self.entityValuesQueryBuilder = ExactAttributeValuesQueryBuilder()


    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        nameQueries = self.entityNamesQueryBuilder.buildQueries(entity, idField)
        valueQueries = self.entityValuesQueryBuilder.buildQueries(entity, idField)
        queries = nameQueries
        queries.extend(valueQueries)

        return queries
