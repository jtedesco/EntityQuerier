from json import load

__author__ = 'jon'

def outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results, append = False, cutoff = 200):
    """
      Give nice formatted output of some search results
    """

    # Find the 'standard' for this entity -- the true list of relevant results
    relevantUrls = load(open(projectRoot + '/standard/' + entityId + '.json'))

    # Prepare vars & data structs
    relevantUrlsFound = []
    count = 0
    precisionAt10 = 0
    precisionAt20 = 0
    precisionAt50 = 0
    precisionAt100 = 0
    recallAt10 = 0
    recallAt20 = 0
    recallAt50 = 0
    recallAt100 = 0

    if len(results) > 0 and type(results[0]) == type({}):
        includesScores = False
    else:
        includesScores = True

    for result in results:
        count += 1
        if count > cutoff:
            break

        # Record if this was a relevant result
        if includesScores:
            if result[1]['url'] in relevantUrls:
                relevantUrlsFound.append(result[1]['url'])
        else:
            if result['url'] in relevantUrls:
                relevantUrlsFound.append(result['url'])


        # Gather precision & recall data
        if count == 10:
            precisionAt10 = float(len(relevantUrlsFound)) / 10
            recallAt10 = float(len(relevantUrlsFound)) / len(relevantUrls)
        elif count == 20:
            precisionAt20 = float(len(relevantUrlsFound)) / 20
            recallAt20 = float(len(relevantUrlsFound)) / len(relevantUrls)
        elif count == 50:
            precisionAt50 = float(len(relevantUrlsFound)) / 50
            recallAt50 = float(len(relevantUrlsFound)) / len(relevantUrls)
        elif count == 100:
            precisionAt100 = float(len(relevantUrlsFound)) / 100
            recallAt100 = float(len(relevantUrlsFound)) / len(relevantUrls)

    # Build the output
    output = outputTitle % cutoff
    output += "Precision @ 10:  %1.5f | Recall @ 10:  %1.5f\n" % (precisionAt10, recallAt10)
    output += "Precision @ 20:  %1.5f | Recall @ 20:  %1.5f\n" % (precisionAt20, recallAt20)
    output += "Precision @ 50:  %1.5f | Recall @ 50:  %1.5f\n" % (precisionAt50, recallAt50)
    output += "Precision @ 100: %1.5f | Recall @ 100: %1.5f\n\n" % (precisionAt100, recallAt100)
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


