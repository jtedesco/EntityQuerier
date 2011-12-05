import mechanize
from mechanize._mechanize import LinkNotFoundError
from pprint import pprint
import re
import sys
from src.search.ResultParserThread import ResultParserThread
from src.search.Search import Search
from BeautifulSoup import BeautifulSoup

__author__ = 'jon'


class GoogleSearch(Search):
    """
      Implements the facade with which to query a specific search engine about the retrieved results
    """

    def query(self, query, fetchContent=True):
        """
          Query the search interface and return a dictionary of results

            @param  query               The query to submit to Google
            @param  fetchContent        Determines whether or not we should fill in information about each result's content

            @return A dictionary representing the search results
        """

        # Start on the first page of results
        googleQuery = str(self.__prepareGoogleQuery(query))
        url = "http://google.com/search?q=" + googleQuery

        shouldStop = False
        results = []

        # Prepare the mechanize browser
#        projectRoot = str(os.getcwd())
#        projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
#        userAgents = load(open(projectRoot + '/userAgents.json'))
        br = mechanize.Browser()
#        randomUserAgent = userAgents[randint(0, len(userAgents)-1)]
        br.addheaders = [('User-agent', "Mozilla/5.0 (Ubuntu; X11; Linux x86_64; rv:8.0) Gecko/20100101 Firefox/8.0")]
        br.set_handle_robots(False)
        response = br.open(url)
        
        if self.verbose:
            print "Querying '%s'..." % query.strip()

        iteration = 0
        while not shouldStop:

            # Add the results from this page
            content = response.read()
            newResults = self.__parseResults(content, fetchContent)
            iteration += 1

            if len(newResults) >= self.numberOfResultsToRetrieve:
                shouldStop = True
            elif len(newResults) == 0:
                shouldStop = True
                print "Stopped parsing results on iteration %d" % iteration

            # Go to the next page
            try:
                links = br.links(text_regex=re.compile("Next"))
                link = links[0]
            except LinkNotFoundError:
                pprint(response.read())
                shouldStop = True
            except:
                print "Do a captcha..."
                var = raw_input()
                br.find_link(text='Next')
                response = br.follow_link(text='Next')

        # Trim the results down to the exact size we want
        results = results[:self.numberOfResultsToRetrieve]

        return results


    def __parseResults(self, resultsContent, fetchContent):
        """
          Parse the results from the HTML content of Google's results page

          The data structure returned, the first returned value holds data as:
          [
            {
                'url': <url>
                'preview' : <preview snippet>
                'title' : <title>
                'description' : <meta description>
                'pageRank' : <PageRank, between 0 and 10>
                'content' : <page content>
            },
            ...
          ]

            @param  resultsContent The HTML content to parse (the results page of Google)
            @return
                results: A dictionary, parsed from the results, that contains the basic result information
        """

        results = []

        # Get the result entries (the list of results)
        parsedHTML = BeautifulSoup(resultsContent)
        resultEntries = parsedHTML.findAll('li', {'class' : 'g'})

        # Add entries, and content for each
        for resultEntry in resultEntries:

            # Extract all the data we can for this result from the main results page
            url = str(resultEntry.find('a').attrs[0][1])

            try:
                preview = resultEntry.find('span', {'class' : 'st'}).text.encode('ascii', 'ignore').lower()
            except AttributeError:
                preview = ""

            # Add it to our results
            result = {
                'url': url,
                'preview': preview
            }
            results.append(result)


        if fetchContent:
            try:
                # Create threads to process the pages for this set of results
                threads = []
                for resultData in results:
                    url = resultData['url']
                    dotLocation = url.rfind('.')
                    if dotLocation != -1 or url[dotLocation:] not in set(['.ps', '.pdf', '.ppt', '.pptx', '.doc', 'docx']):
                        parserThread = ResultParserThread(resultData, self.verbose, self.extensions)
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
                        except Exception:
                            print(str(thread.getName()) + ' could not be terminated')


            except Exception:

                if self.verbose:
                    print "Error parsing basic results from Google: '%s'" % str(sys.exc_info()[1]).strip()

        return results


    def __prepareGoogleQuery(self, query):
        """
          Cleans up a query string before submission to Google

            @param  query   The query to clean
            @return The 'cleaned' query
        """

        query = query.replace('+', '%2B')
        query = query.replace(' ', '+')
        query = query.replace('~', '%7E')

        return query

