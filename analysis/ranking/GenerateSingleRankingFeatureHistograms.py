"""
  Generates grouped histograms comparing the effects of DMOZ smoothing on a basic BM25 ranking
"""
import os
import subprocess
from analysis.VisualizationUtility import splitCamelCase, averageEntityScores, populateData

__author__ = 'jon'



if __name__ == '__main__':

    # A map of entity names -> experiments -> metrics
    data = {}

    # Find the project root
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

    # Iterate through each result directory
    rootVisualizationDirectory = projectRoot + '/experiments/ranking/results'
    populateData(data, rootVisualizationDirectory)
    del data['dmoz'] # ignore dmoz results

    averageScores = averageEntityScores(data)

    # Concatenate the names of metrics for the horizontal
    experiments = {
        'BM25BaselineRanking': 'Baseline Google Ranking',
        'BM25Ranking': 'BM25 Content',
        'BM25DescriptionRanking': 'BM25 Content & Description',
        'BM25ExpandedYahooKeywordsRanking': 'BM25 Content & Expanded Yahoo Keywords',
        'BM25HeadersRanking': 'BM25 Content & Headers',
        'BM25KeywordsRanking': 'BM25 Content & Keywords',
        'BM25PageRankRanking': 'BM25 Content & PageRank',
        'BM25TitleRanking': 'BM25 Content & Title',
        'BM25YahooKeywordsRanking': 'BM25 Content & Yahoo Keywords'
    }

    for experiment in experiments:
        if experiment not in {'BM25BaselineRanking', 'BM25Ranking'}:

            # The order in which the groups of histograms should appear
            sortedExperiments = [
                'BM25Ranking',
                experiment,
                'BM25BaselineRanking'
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
            configurationFile = projectRoot + '/analysis/configurations/single_ranking_feature_clustered_histograms'
            configuration = open(configurationFile).read()

            # Fill out the configuration
            newFeature = experiments[experiment].split('&')[1][1:].strip()
            configuration = configuration % (
                projectRoot + '/analysis/output/%sRankingFeature.png' % newFeature.replace(' ', ''),
                'Effect of %s of Results on Ranking' % newFeature,
                'Ranking Strategies'
            )
            open('config', 'w').write(configuration)

            # Run gnuplot
            subprocess.Popen(['gnuplot', 'config']).communicate()

            os.remove('config')
            os.remove('input.dat')