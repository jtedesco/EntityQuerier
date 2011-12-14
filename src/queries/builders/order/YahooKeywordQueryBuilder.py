from json import loads
from pprint import pprint
from src.queries.builders.QueryBuilder import QueryBuilder
from src.search.SearchResultParsing import loadFromUrl
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from util.YQLCache import YQLCache

__author__ = 'jon'


class YahooKeywordQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every relevant keyword returned from Yahoo for an entity description
    """

    def __init__(self):
        
        # Cache the data retrieved
        self.cache = YQLCache()

        self.apiUrl = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20search.termextract%20where%20context%3D%22####%22&format=json'


    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        entityId = entity[idField]

        # Get the lists of name & value queries
        attributeNames = self.getAttributeNames(entity, idField)
        attributeValues = self.getAttributeValues(entity, idField)
        attributeNamesAndValues = set(attributeNames).union(set(attributeValues))
        attributeNamesAndValues.remove(entityId)

        # Generate the text
        entityDescription = ', '.join(attributeNamesAndValues)

        # Get the Yahoo keywords for this entity
        keywords = self.extractKeywords(entityDescription)

        # Build the queries
        queries = [entityId]
        for keyword in keywords:
            queries.append(entityId + ' ' + keyword)

        pprint(queries)

        return queries


    def getAttributeNames(self, entity, idField):

        attributeNames = []

        # Generate queries for each data entry
        for property in entity:
            if property is not idField:
                attributeNames.append(str(property))

        return attributeNames


    def getAttributeValues(self, entity, idField):

        attributeValues = []

        # Generate queries for each data entry
        for property in entity:
            if property is not idField:

                # Get the property
                entityProperty = entity[property]
                if entityProperty is not None:

                    # Generate a query for each entry in a list
                    if type(entityProperty) == type([]):
                        for property in entityProperty:
                            attributeValues.append(str(property))
                    elif entityProperty is not None:
                        attributeValues.append(str(entityProperty))

        return attributeValues

    
    def extractKeywords(self, entityDescription):
        """
          Retrieve the set of keywords for the entity description
        """

        keywords = set([])

        # Fill the URL template
        url = self.apiUrl.replace('####', entityDescription)
        url = url.replace(' ', '%20')

        # Get the keyword data, from the cache if possible
        keywordJson = self.cache.read(url)
        if keywordJson is None:
            keywordJson = loadFromUrl(url)
            self.cache.write(url, keywordJson)
        keywordData = loads(keywordJson)
        try:
            fetchedKeywords = keywordData['query']['results'].values()
            keywords = keywords.union(set(fetchedKeywords[0]))
        except AttributeError:
            pass

        return list(keywords)
