from json import load

__author__ = 'jon'

def outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results, append = False, cutoff = 200):
    """
      Give nice formatted output of some search results
    """

    if len(results) > 0 and type(results[0]) == type({}):
        includesScores = False
    else:
        includesScores = True

    # Find the 'standard' for this entity -- the true list of relevant results
    relevantUrls = load(open(projectRoot + '/standard/' + entityId + '.json'))

    recallAt1, recallAt10, recallAt20, recallAt50, precisionAt1, precisionAt10, precisionAt20, precisionAt50, \
        averagePrecisionAt1, averagePrecisionAt10, averagePrecisionAt20, averagePrecisionAt50, rPrecision, fullPrecision = getRankingResults(results, relevantUrls, cutoff)

    # Build the output
    output = outputTitle % cutoff
    output += "Precision @ 1:  %1.5f | Average Precision @ 1:  %1.5f\n" % (precisionAt1, averagePrecisionAt1)
    output += "Precision @ 10:  %1.5f | Average Precision @ 10:  %1.5f\n" % (precisionAt10, averagePrecisionAt10)
    output += "Precision @ 20:  %1.5f | Average Precision @ 20:  %1.5f\n" % (precisionAt20, averagePrecisionAt20)
    output += "Precision @ 50: %1.5f | Average Precision @ 50:  %1.5f\n\n" % (precisionAt50, averagePrecisionAt50)
    output += "Recall @ 50: %1.5f | R-Precision:  %1.5f | Precision at 100 Percent (full) Recall Point: %1.5f\n\n" % (recallAt50, rPrecision, fullPrecision)
    output += "Score         Url\n"
    output += "=====         ===\n"
    count = 0
    if includesScores:
        for score, result in results:
            count += 1
            if count > cutoff:
                break
            output += "%1.5f       %s\n" % (score, result['url'])
    else:
        for result in results:
            count += 1
            if count > cutoff:
                break
            output += "??????       %s\n" % result['url']
    output += "\n\n\n"

    # Write it out a file
    if append:
        open(projectRoot + '/experiments/ranking/results/' + outputFile, 'a').write(output)
    else:
        open(projectRoot + '/experiments/ranking/results/' + outputFile, 'w').write(output)


def getRankingResults(results, relevantUrls, cutoff):

    # Prepare vars & data structs
    relevantUrlsFound = []
    count = 0
    precisionAt1 = 0
    precisionAt10 = 0
    precisionAt20 = 0
    precisionAt50 = 0
    recallAt1 = 0
    recallAt10 = 0
    recallAt20 = 0
    recallAt50 = 0
    averagePrecisionAt1 = 0
    averagePrecisionAt10 = 0
    averagePrecisionAt20 = 0
    averagePrecisionAt50 = 0
    rPrecision = 0


    if len(results) > 0 and type(results[0]) == type({}):
        includesScores = False
    else:
        includesScores = True

    averagePrecisionRunningTotal = 0.0
    fullPrecision = 0
    for result in results:
        count += 1
        if count > cutoff:
            break

        # Record if this was a relevant result
        wasRelevant = False
        if includesScores:
            if result[1]['url'] in relevantUrls:
                wasRelevant = True
                relevantUrlsFound.append(result[1]['url'])
        else:
            if result['url'] in relevantUrls:
                wasRelevant = True
                relevantUrlsFound.append(result['url'])

        # Precision at 100% recall point
        if wasRelevant:
            fullPrecision = float(len(relevantUrlsFound)) / count

        # Update running total for average precision
        if wasRelevant:
            averagePrecisionRunningTotal += float(len(relevantUrlsFound)) / count

        # Gather precision & recall data
        if count == 1:
            precisionAt1 = float(len(relevantUrlsFound))
            recallAt1 = float(len(relevantUrlsFound)) / len(relevantUrls)
            try:
                averagePrecisionAt1 = averagePrecisionRunningTotal / len(relevantUrlsFound)
            except ZeroDivisionError:
                averagePrecisionAt1 = 0
        elif count == 10:
            precisionAt10 = float(len(relevantUrlsFound)) / 10
            recallAt10 = float(len(relevantUrlsFound)) / len(relevantUrls)
            try:
                averagePrecisionAt10 = averagePrecisionRunningTotal / len(relevantUrlsFound)
            except ZeroDivisionError:
                averagePrecisionAt10 = 0
        elif count == 20:
            precisionAt20 = float(len(relevantUrlsFound)) / 20
            recallAt20 = float(len(relevantUrlsFound)) / len(relevantUrls)
            try:
                averagePrecisionAt20 = averagePrecisionRunningTotal / len(relevantUrlsFound)
            except ZeroDivisionError:
                averagePrecisionAt20 = 0
        elif count == 50:
            precisionAt50 = float(len(relevantUrlsFound)) / 50
            recallAt50 = float(len(relevantUrlsFound)) / len(relevantUrls)
            try:
                averagePrecisionAt50 = averagePrecisionRunningTotal / len(relevantUrlsFound)
            except ZeroDivisionError:
                averagePrecisionAt50 = 0

        # r-precision
        if count == len(relevantUrls):
            rPrecision = float(len(relevantUrlsFound)) / count

    return recallAt1, recallAt10, recallAt20, recallAt50, precisionAt1, precisionAt10, precisionAt20, precisionAt50,\
           averagePrecisionAt1, averagePrecisionAt10, averagePrecisionAt20, averagePrecisionAt50, rPrecision, fullPrecision
