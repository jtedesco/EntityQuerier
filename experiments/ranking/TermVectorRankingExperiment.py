from json import load
import os
from experiments.RankingExperiment import RankingExperiment
from src.ranking.TermVectorRanking import TermVectorRanking

__author__ = 'jon'


if __name__ == '__main__':

    # Find the project root & open the input entity
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
    entity = load(open(projectRoot + '/entities/Kevin Chen-Chuan Chang.json'))

    # Rank the results
    rankingExperiment = RankingExperiment(projectRoot + '/experiments/retrieval/results/KevinChang-EntityNamesAndValuesWithOperators', entity, TermVectorRanking)
    results = rankingExperiment.rank()

    # Measure the precision & recall at 10, 20, and 50
    relevantUrls = load(open(projectRoot + '/standard/Kevin Chen-Chuan Chang.json'))
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
    for result in results:
        count += 1
        if count > 200:
            break

        # Record if this was a relevant result
        if result[1]['url'] in relevantUrls:
            relevantUrlsFound.append(result[1]['url'])

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
    output = "Term Vector Ranking Results Summary (for top 200 results):\n"
    output += "Precision @ 10:  %1.5f | Recall @ 10:  %1.5f\n" % (precisionAt10, recallAt10)
    output += "Precision @ 20:  %1.5f | Recall @ 20:  %1.5f\n" % (precisionAt20, recallAt20)
    output += "Precision @ 50:  %1.5f | Recall @ 50:  %1.5f\n" % (precisionAt50, recallAt50)
    output += "Precision @ 100: %1.5f | Recall @ 100: %1.5f\n\n" % (precisionAt100, recallAt100)
    output +=  "Score         Url\n"
    output += "=====         ===\n"
    count = 0
    for score, result in results:
        count += 1
        if count > 200:
            break
        output += "%1.5f       %s\n" % (score, result['url'])

    # Write it out a file
    open(projectRoot + '/experiments/ranking/results/KevinChang-TermVectorRanking', 'w').write(output)
    
