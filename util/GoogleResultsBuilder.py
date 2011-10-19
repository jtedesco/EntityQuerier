from src.search.google.GoogleResultParserThread import GoogleResultParserThread

__author__ = 'jon'

def buildResultsFromURLs(urls, fetchContent=True):
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

    if fetchContent:

        # Create threads to process the pages for this set of results
        threads = []
        for resultData in results:
            parserThread = GoogleResultParserThread(resultData)
            threads.append(parserThread)

        # Launch all threads
        for thread in threads:
            thread.start()

        # Wait for all the threads to finish
        for thread in threads:
            thread.join()

    return results
