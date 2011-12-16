__author__ = 'jon'


def getKeywords(entity):
    """
      Retrieve list of lowercase values for an entity description
    """

    keywords = []
    for key in entity:
        keywords.extend(key.split())
        if type(entity[key]) == type([]):
            for keyword in entity[key]:
                if keyword is not None:
                    lowercaseKeyword = keyword.lower()
                    if len(lowercaseKeyword.split()) > 1:
                        keywords.append(lowercaseKeyword)
                        keywords.extend(lowercaseKeyword.split())
                    else:
                        keywords.append(lowercaseKeyword)
        else:
            keyword = entity[key]
            if keyword is not None:
                lowercaseKeyword = keyword.lower()
                if len(lowercaseKeyword.split()) > 1:
                    keywords.append(lowercaseKeyword)
                    keywords.extend(lowercaseKeyword.split())
                else:
                    keywords.append(lowercaseKeyword)
    return keywords


def group(results, groupSize):
    return [results[i : i + groupSize] for i in xrange(0, len(results), groupSize)]