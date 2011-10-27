def recallQueryScore(newRelevantResults, duplicateRelevantResults, nonRelevantNewResults,
                                 relevantResultsSoFar, resultsSoFar,
                                 totalRelevantDocumentsRetrieved, totalRelevantDocumentsNotRetrieved):
    """
      Returns the recall score of the series of queries if this query is performed.
    """

    # Compute the recall of the series of queries if this query is performed
    relevantDocuments = set(totalRelevantDocumentsRetrieved).union(set(totalRelevantDocumentsNotRetrieved))
    try:
        queryScore = len(set(relevantResultsSoFar).union(newRelevantResults)) /                                     \
                     float(len(relevantDocuments))
    except ZeroDivisionError:
        queryScore = 0.0

    return queryScore


def precisionQueryScore(newRelevantResults, duplicateRelevantResults, nonRelevantNewResults,
                                 relevantResultsSoFar, resultsSoFar,
                                 totalRelevantDocumentsRetrieved, totalRelevantDocumentsNotRetrieved):
    """
      Returns the precision of the series of queries after this query is performed.
    """

    # Compute the precision if this query is performed
    queryResults = set(newRelevantResults).union(set(duplicateRelevantResults)).union(set(nonRelevantNewResults))
    try:
        queryScore = len(set(relevantResultsSoFar).union(newRelevantResults)) /                                     \
                     float(len(queryResults.union(set(resultsSoFar))))
    except ZeroDivisionError:
        queryScore = 0.0

    return queryScore


def combinedRecallAndPrecisionQueryScore(newRelevantResults, duplicateRelevantResults, nonRelevantNewResults,
                                 relevantResultsSoFar, resultsSoFar,
                                 totalRelevantDocumentsRetrieved, totalRelevantDocumentsNotRetrieved,
                                 recallWeight = 0.5):
    """
      Implements a combined recall & precision scoring scheme, which computes the query score by averaging
        the recall.
    """

    # Compute the recall & precision
    recall = recallQueryScore(newRelevantResults, duplicateRelevantResults, nonRelevantNewResults,
                                 relevantResultsSoFar, resultsSoFar,
                                 totalRelevantDocumentsRetrieved, totalRelevantDocumentsNotRetrieved)
    precision = precisionQueryScore(newRelevantResults, duplicateRelevantResults, nonRelevantNewResults,
                                 relevantResultsSoFar, resultsSoFar,
                                 totalRelevantDocumentsRetrieved, totalRelevantDocumentsNotRetrieved)

    queryScore = ((1.0 - recallWeight) * precision) + (recallWeight * recall)
    return queryScore
