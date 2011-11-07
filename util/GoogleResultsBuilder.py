from src.search.google.GoogleResultParserThread import GoogleResultParserThread

__author__ = 'jon'

def buildGoogleResultsFromURLs(urls, fetchContent=True, verbose=False):
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
            parserThread = GoogleResultParserThread(resultData, verbose)
            threads.append(parserThread)

    # Launch all threads
    for thread in threads:
        thread.start()

    # Wait for all the threads to finish
    for thread in threads:
        thread.join()


    return results
