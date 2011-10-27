from src.queries.QueryBuilder import QueryBuilder

__author__ = 'jon'


class EntityAttributeValuesQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity
    """

    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        queries = ["\"%s\"" % entity[idField]]

        # Get the uniquely identifying key for this entity
        entityKey = entity[idField]

        # Generate queries for each data entry
        for property in entity:
            if property is not idField:

                # Get the property
                entityProperty = entity[property]
                if entityProperty is not None:

                    # Generate a query for each entry in a list
                    if type(entityProperty) == type([]):
                        for property in entityProperty:
                            queries.append('"' + str(entityKey) + '" "' + str(property) + '"')
                    else:
                        queries.append('"' + str(entityKey) + '" "' + str(entityProperty) + '"')

        return queries
