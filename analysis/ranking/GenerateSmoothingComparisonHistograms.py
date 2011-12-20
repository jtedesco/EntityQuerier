"""
  Generates grouped histograms comparing the effects of DMOZ smoothing on a basic BM25 ranking
"""
import os
import subprocess
from analysis.VisualizationUtility import splitCamelCase, averageEntityScores, populateRankingData

__author__ = 'jon'

if __name__ == '__main__':

    # A map of entity names -> experiments -> metrics
    data = {}

    # Find the project root
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

    # Iterate through each result directory
    rootVisualizationDirectory = projectRoot + '/experiments/ranking/results/dmoz'
    populateRankingData(data, rootVisualizationDirectory)

    averageScores = averageEntityScores(data)

    # Concatenate the names of metrics for the horizontal
    dataContent = "Experiment "
    sortedAverageScores = [
        ('BM25Ranking', 'None'),
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
        projectRoot + '/analysis/output/ranking/DMOZSmoothingEffect.png',
        'Effect of Adding DMOZ Documents on BM25 Performance',
        'Number of Non-relevant DMOZ Documents'
    )
    open('config', 'w').write(configuration)

    # Run gnuplot
    subprocess.Popen(['gnuplot', 'config']).communicate()

    os.remove('config')
    os.remove('input.dat')