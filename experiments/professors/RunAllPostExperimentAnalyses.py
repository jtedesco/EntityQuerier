import os
import subprocess
from experiments.PostExperimentAnalysis import PostExperimentAnalysis

__author__ = 'jon'


if __name__ == '__main__':

    # Find the absolute path to the script to get the output of an analysis
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
    scriptPath = projectRoot
    scriptPath += "/experiments/PostExperimentAnalysis.py"
    pageRankScriptPath = scriptPath

    for fileName in os.listdir(projectRoot + '/experiments/professors/results'):

        # Run the analysis
        filePath = projectRoot + '/experiments/professors/results/' + str(fileName)
        analysis = PostExperimentAnalysis(filePath)

        # Get the results together
        results = subprocess.check_output(["python", scriptPath, filePath])
        open(projectRoot + '/experiments/professors/analyses/' + str(fileName), 'w').write(results)
