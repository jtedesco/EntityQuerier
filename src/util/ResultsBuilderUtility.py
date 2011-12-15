from json import loads, load
import os
from src.search.ResultParserThread import ResultParserThread

__author__ = 'jon'


def buildGoogleResultsFromURLs(urls, fetchContent=True, verbose=False, extensions=[]):
    """
      Builds a list of results in the same format as those retrieved from a search engine, using a list of URLs to populate
        the results.
    """

    # Build the formatted list of results
    results = []
    for url in urls:
        results.append({
            'url' : url
        })

    # Create threads to process the pages for this set of results
    threads = []
    for resultData in results:
        url = resultData['url']
        dotLocation = url.rfind('.')
        if dotLocation != -1 or url[dotLocation:] not in {'.ps', '.pdf', '.ppt', '.pptx', '.doc', 'docx'} and fetchContent:
            parserThread = ResultParserThread(resultData, verbose, extensions)
            threads.append(parserThread)

    # Launch all threads
    for thread in threads:
        thread.start()

    # Wait for all the threads to finish
    for thread in threads:

        # Allow up to 5 seconds for this thread to respond, otherwise, kill it
        thread.join(5)

        # Kill it if it hung
        if thread.isAlive():
            try:
                thread._Thread__stop()
            except:
                print(str(thread.getName()) + ' could not be terminated')


    return results


def getResultsFromRetrievalFile(path, extensions):

    # Get the contents of the file
    resultsData = open(path).read()

    # Strip off the header
    dataToBeJoined = []
    recordData = False
    for dataLine in resultsData.split('\n'):
        if not recordData and len(dataLine) > 0 and dataLine[0] == '{':
            recordData = True
        if recordData:
            dataToBeJoined.append(dataLine)
    resultsData = '\n'.join(dataToBeJoined)

    # Load the data dumped from the first stage
    resultsDump = loads(resultsData)

    # Initialize the extensions (HACK)
    for extension in extensions:
        if 'initialize' in dir(extension):
            extension.initialize(resultsDump)

    # Build the data structure that will map entity id -> urls
    entityUrls = set([])
    for query in resultsDump:
        for resultType in resultsDump[query]:
            for url in resultsDump[query][resultType]:
                if url not in ['precision', 'recall', 'averagePrecision']:
                    entityUrls.add(url)

    results = buildGoogleResultsFromURLs(entityUrls, True, True, extensions)

    return results


def getDmozResults():

    # Find where we expect this data to be cached
    dmozPath = str(os.getcwd())
    dmozPath = dmozPath[:dmozPath.find('EntityQuerier') + len('EntityQuerier')] + '/dmoz/'

    # Supplement the index with the DMOZ documents
    dmozResults = []
    for filename in os.listdir(dmozPath):

        try:

            # Get the contents of the file
            dmozResultFile = open(dmozPath + filename)
            dmozResult = load(dmozResultFile)
            dmozResults.append(dmozResult)

        except ValueError:

            # Do something awful...
            try:
                dmozResult = eval(dmozResultFile.read())
                dmozResults.append(dmozResult)
            except Exception:
                pass

    # Create the index with both the traditional and new DMOZ search results
    return dmozResults


def getResultsFromEntityId(entityId, retrievalExperimentName, extensions):

    # Find the project root
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

    # Find the results path
    entityName = entityId.replace(' ', '').replace('-', '')
    resultsFilePath = projectRoot + '/experiments/retrieval/results/%s/%s' % (entityName, retrievalExperimentName)

    return getResultsFromRetrievalFile(resultsFilePath, extensions)
