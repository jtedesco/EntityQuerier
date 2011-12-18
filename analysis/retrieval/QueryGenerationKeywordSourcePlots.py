"""
  Generates grouped histograms comparing the effects of DMOZ smoothing on a basic BM25 ranking
"""
import os
from pprint import pprint
import subprocess
import sys
from analysis.VisualizationUtility import splitCamelCase, averageEntityScores, populateRankingData, populateRetrievalData

__author__ = 'jon'


def generatePointPlots(averageScores, experiments, projectRoot):
    """
      Generate the plot of points
    """


    dataContent = 'Experiment "Number of Queries" "Total Recall"\n'

    for experiment in experiments:
        dataContent += '"%s" %1.5f %1.5f\n\n\n' % (
        experiments[experiment], averageScores[experiment]['numberOfQueries'], averageScores[experiment]['recall'])

    # Write it out to the input file to gnuplot
    open("input.dat", 'w').write(dataContent)

    # Get the configuration
    configurationFile = projectRoot + '/analysis/configurations/query_total_recall_efficiency_plot'
    configuration = open(configurationFile).read()

    # Fill out the configuration
    configuration = configuration % tuple([
                                              projectRoot + '/analysis/output/retrieval/QueryGenerationKeywordsPlot.png'
                                              ,
                                              'Total Recall Efficiency of Keyword Sources for Query Generation Strategy'
                                              ,
                                              'Number of Queries',
                                              'Total Recall'
                                          ] + experiments.values())
    open('config', 'w').write(configuration)

    # Run gnuplot
    subprocess.Popen(['gnuplot', 'config']).communicate()
    os.remove('config')
    os.remove('input.dat')


def generateNumberQueriesHistogramPlots(averageScores, projectRoot):
    """
      Generate histogram-style plots for the query generation keyword source experiments
    """

    sortedExperiments = [
        'AttributeNamesAndValues',
        'AttributeValues',
        'AttributeNames',
        'YahooKeywords',
    ]

    sortedMetrics = [
        'numberOfQueries'
    ]

    dataContent = "Experiment "
    for experiment in sortedExperiments:
        dataContent += '"' + splitCamelCase(experiment).title().replace('&', 'and') + '" '
    dataContent += '\n'

    # Build the results for this experiment
    for metric in sortedMetrics:
        dataContent += '"' + splitCamelCase(metric).title().replace('&', 'and') + '" '
        for experiment in sortedExperiments:
            dataContent += str(averageScores[experiment][metric]) + ' '
        dataContent += '\n'

    # Write it out to the input file to gnuplot
    open("input.dat", 'w').write(dataContent)

    # Get the configuration
    configurationFile = projectRoot + '/analysis/configurations/query_number_queries_histograms'
    configuration = open(configurationFile).read()
    configuration = configuration % (
        projectRoot + '/analysis/output/retrieval/QueryGenerationKeywordsNumberHistogram.png',
        'Comparison of Number of Queries for Query Expansion Keyword Selection Strategies',
        'Query Generation Strategy',
        'Number of Queries'
    )
    open('config', 'w').write(configuration)

    # Run gnuplot
    subprocess.Popen(['gnuplot', 'config']).communicate()

    os.remove('config')
    os.remove('input.dat')


def generatePrecisionRecallHistogramPlots(averageScores, projectRoot):
    """
      Generate histogram-style plots for the query generation keyword source experiments
    """

    sortedExperiments = [
        'AttributeNames',
        'YahooKeywords',
        'AttributeValues',
        'AttributeNamesAndValues'
    ]

    sortedMetrics = [
        'recall',
        'precision'
    ]

    # Generate the header for the metrics
    dataContent = "Experiment "
    for experiment in sortedExperiments:
        dataContent += '"' + splitCamelCase(experiment).title().replace('&', 'and') + '" '
    dataContent += '\n'

    # Build the results for this experiment
    for metric in sortedMetrics:
        dataContent += '"' + splitCamelCase(metric).title().replace('&', 'and') + '" '
        for experiment in sortedExperiments:
            dataContent += str(averageScores[experiment][metric]) + ' '
        dataContent += "\n"

    # Write it out to the input file to gnuplot
    open("input.dat", 'w').write(dataContent)

    # Get the configuration
    configurationFile = projectRoot + '/analysis/configurations/query_precision_recall_histograms'
    configuration = open(configurationFile).read()
    configuration = configuration % (
        projectRoot + '/analysis/output/retrieval/QueryGenerationKeywordsPrecisionRecallHistogram.png',
        'Comparison of Precision and Recall for Query Expansion Keyword Selection Strategies',
        'Query Generation Metric',
        )
    open('config', 'w').write(configuration)

    # Run gnuplot
    subprocess.Popen(['gnuplot', 'config']).communicate()

    os.remove('config')
    os.remove('input.dat')


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
        'YahooKeywords': 'Yahoo Keywords'
    }

    # Build the point plots
    generatePointPlots(averageScores, experiments, projectRoot)

    # Build the histogram plots
    generateNumberQueriesHistogramPlots(averageScores, projectRoot)
    generatePrecisionRecallHistogramPlots(averageScores, projectRoot)

    # TODO: Build the baseline recall / precision histograms
    # TODO: Build the baseline number of queries histograms