"""
  Generates grouped histograms comparing the effects of DMOZ smoothing on a basic BM25 ranking
"""
import os
import subprocess
from analysis.VisualizationUtility import splitCamelCase, parseStatsFromRanking, averageEntityScores

__author__ = 'jon'

if __name__ == '__main__':

    # A map of entity names -> experiments -> metrics
    data = {}

    # Find the project root
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

    # Iterate through each result directory
    rootVisualizationDirectory = projectRoot + '/experiments/ranking/results/dmoz'
    for folder in os.listdir(rootVisualizationDirectory):

        entityName = folder
        entityDirectory = rootVisualizationDirectory + '/' + folder

        data[entityName] = {}

        if os.path.isdir(entityDirectory):
            for experimentFile in os.listdir(entityDirectory):

                experimentName = experimentFile

                # Parse the data from the ranking output
                precisionAt1, precisionAt10, precisionAt20, precisionAt50, averagePrecisionAt1, averagePrecisionAt10, \
                    averagePrecisionAt20,  averagePrecisionAt50, recallAt50, rPrecision, fullPrecision = parseStatsFromRanking(entityDirectory + '/' + experimentFile)
                
                # Insert all these data points
                data[entityName][experimentName] = {
                    'precisionAt1' : precisionAt1,
                    'precisionAt10' : precisionAt10,
                    'precisionAt20' : precisionAt20,
                    'precisionAt50' : precisionAt50,
                    'averagePrecisionAt1' : averagePrecisionAt1,
                    'averagePrecisionAt10' : averagePrecisionAt10,
                    'averagePrecisionAt20' : averagePrecisionAt20,
                    'averagePrecisionAt50' : averagePrecisionAt50,
                    'recallAt50' : recallAt50,
                    'rPrecision' : rPrecision,
                    'fullPrecision' : fullPrecision
                }

    averageScores = averageEntityScores(data)

    # Concatenate the names of metrics for the horizontal
    dataContent = "Experiment "
    sortedAverageScores = [
        ('BM25Ranking', 'No Smoothing'),
        ('DMOZSmoothed500BM25Ranking', '500 Documents'),
        ('DMOZSmoothed1000BM25Ranking', '1000 Documents'),
        ('DMOZSmoothed5000BM25Ranking', '5000 Documents'),
        ('DMOZSmoothed1000BM25Ranking', '10000 Documents')
    ]
    sortedMetrics = averageScores[sortedAverageScores[0][0]].keys()
    sortedMetrics.sort()
    for metric in sortedMetrics:
        dataContent += '"' + splitCamelCase(metric).title() + '" '
    dataContent += '\n'
    for experiment in sortedAverageScores:
        dataContent += '"' + experiment[1] + '" '
        for metric in sortedMetrics:
            dataContent += str(averageScores[experiment[0]][metric]) + ' '
        dataContent += "\n"

    # Write it out to the input file to gnuplot
    open("input.dat", 'w').write(dataContent)

    # Get the configuration
    configurationFile = projectRoot + '/analysis/configurations/smoothing_clustered_histograms'
    configuration = open(configurationFile).read()

    # Fill out the configuration
    configuration = configuration % (
        projectRoot + '/analysis/output/DMOZSmoothingEffect.png',
        'Effect of DMOZ Smoothing on BM25 Performance',
        'DMOZ Smoothing'
    )
    open('config', 'w').write(configuration)

    # Run gnuplot
    subprocess.Popen(['gnuplot', 'config']).communicate()