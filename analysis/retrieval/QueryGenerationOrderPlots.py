"""
  Generates grouped histograms comparing the effects of DMOZ smoothing on a basic BM25 ranking
"""
import os
from pprint import pprint
import subprocess
import sys
from analysis.VisualizationUtility import splitCamelCase, averageEntityScores, populateRankingData, populateRetrievalData

__author__ = 'jon'



if __name__ == '__main__':

    # A map of entity names -> experiments -> metrics
    data = {}

    # Find the project root
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

    # Iterate through each result directory
    rootVisualizationDirectory = projectRoot + '/experiments/retrieval/results'
    populateRetrievalData(data, rootVisualizationDirectory)
    averageScores = averageEntityScores(data)

    # Concatenate the names of metrics for the horizontal
    experiments = {
        'AttributeNames': 'Attribute Names',
        'AttributeNamesAndValues': 'Attribute Names and Values',
        'AttributeValues': 'Attribute Values',
        'WordNetPolysemy10': 'Top 10 Ordered Queries',
        'WordNetPolysemy15': 'Top 15 Ordered Queries',
        'WordNetPolysemy20': 'Top 20 Ordered Queries',
    }

    dataContent = 'Experiment "Number of Queries" "Total Recall"\n'
    plot = ""

    sortedExperiments = experiments.keys()
    sortedExperiments.sort()

    values = []
    for experiment in sortedExperiments:
        dataContent += '"%s" %1.5f %1.5f\n\n\n' % (experiments[experiment], averageScores[experiment]['numberOfQueries'], averageScores[experiment]['recall'])
        values.append(experiments[experiment])

    # Write it out to the input file to gnuplot
    open("input.dat", 'w').write(dataContent)

    # Get the configuration
    configurationFile = projectRoot + '/analysis/configurations/large_query_total_recall_efficiency_plot'
    configuration = open(configurationFile).read()

    # Fill out the configuration
    configuration = configuration % tuple([
        projectRoot + '/analysis/output/QueryGenerationOrder.png',
        'Total Recall Efficiency of Keyword Sources With Ordered Keywords for Query Generation Strategy',
        'Number of Queries',
        'Total Recall'
    ] + values)
    open('config', 'w').write(configuration)

    # Run gnuplot
    subprocess.Popen(['gnuplot', 'config']).communicate()

    os.remove('config')
    os.remove('input.dat')