from src.queries.builders.QueryBuilder import QueryBuilder

__author__ = 'jon'


class ExactEntityIdQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity
    """

    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        entityIdQuery = "\"%s\"" % str(entity[idField])
        queries = [entityIdQuery]
        return queries
