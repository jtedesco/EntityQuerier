"""
  Generates grouped histograms comparing the effects of DMOZ smoothing on a basic BM25 ranking
"""
import os
from pprint import pprint
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
    rootVisualizationDirectory = projectRoot + '/experiments/ranking/results'
    populateRankingData(data, rootVisualizationDirectory)
    del data['dmoz'] # ignore dmoz results

    averageScores = averageEntityScores(data)

    # Concatenate the names of metrics for the horizontal
    experiments = {
        'BM25BaselineRanking': 'Baseline Google Ranking',
        'BM25Ranking': 'BM25 Content',
        'RankSVMRanking': 'RankSVM'
    }

    for experiment in experiments:
        if experiment not in {'BM25BaselineRanking', 'BM25Ranking'}:

            # The order in which the groups of histograms should appear
            sortedExperiments = [
                'BM25Ranking',
                'BM25BaselineRanking',
                experiment,
            ]

            # Sort the metrics too
            sortedMetrics = averageScores[experiment].keys()
            sortedMetrics.sort()

            # Generate the header for the metrics
            dataContent = "Experiment "
            for metric in sortedMetrics:
                dataContent += '"' + splitCamelCase(metric).title().replace('&', 'and') + '" '
            dataContent += '\n'

            # Build the results for this experiment
            for drawnExperiment in sortedExperiments:
                dataContent += '"' + experiments[drawnExperiment].replace('&', 'and') + '" '
                for metric in sortedMetrics:
                    dataContent += str(averageScores[drawnExperiment][metric]) + ' '
                dataContent += "\n"

            # Write it out to the input file to gnuplot
            open("input.dat", 'w').write(dataContent)

            # Get the configuration
            configurationFile = projectRoot + '/analysis/configurations/learned_ranking_clustered_histograms'
            configuration = open(configurationFile).read()

            # Fill out the configuration
            configuration = configuration % (
                projectRoot + '/analysis/output/%sLearnedRanking.png' % experiments[experiment].replace(' ', ''),
                'Ranking Strategies',
                'Performance of %s Learned Ranking' % experiments[experiment],
            )
            open('config', 'w').write(configuration)

            # Run gnuplot
            subprocess.Popen(['gnuplot', 'config']).communicate()

            os.remove('config')
            os.remove('input.dat')