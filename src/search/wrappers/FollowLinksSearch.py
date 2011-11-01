import re
from src.search.Search import Search
from src.search.google.GoogleResultParserThread import GoogleResultParserThread
from src.search.google.GoogleSearch import GoogleSearch
from BeautifulSoup import BeautifulSoup
from pprint import pprint

__author__ = 'jon'

class FollowLinksSearch(Search):
    """
      This class allows us to augment results by retrieving links from the first pages of each query
    """

    def __init__(self, searchScheme = GoogleSearch(), numberOfResultsToRetrieve=50, verbose=True, topResultsToFollowLinks=5):
        """
          Initializes this search object
        """

        Search.__init__(self, numberOfResultsToRetrieve, verbose)
        self.searchScheme = searchScheme
        self.topResultsToFollowLinks = topResultsToFollowLinks


    def query(self, query, fetchContent=True):

        # Get the search results from the 'concrete' scheme
        searchResults = self.searchScheme.query(query, fetchContent)

        resultPages = list(searchResults)

        # Follow the links on the top results
        for i in xrange(0, self.topResultsToFollowLinks):

            # Find the links from the top results
            theseResults = self.__getResultsFromPageLinks(resultPages[i]['content'], fetchContent, resultPages[i]['url'])
            resultPages.extend(theseResults)

        return resultPages

    
    def __getResultsFromPageLinks(self, content, fetchContent, url):
        """
          Parse the links from the page content to find these links, using the Google results parser thread

            @param  content The HTML page content from which to grab links
        """
        results = []

        # Extract urls for this page
        parsedContent = BeautifulSoup(content)
        urlTags = parsedContent.findAll('a')
        anchorTextTags = parsedContent.findAll('a')

        # Get the links & anchor text from this site
        urlsFound = []
        for items in zip(urlTags, anchorTextTags):

            # Get the URL & anchor text
            newUrl = items[0].attrs[0][1]
            description = items[1].attrs[0][0]
            anchorTextTags.append(description)

            # Get the absolute URL
            absoluteUrls = self.__buildAbsoluteLinks([newUrl], url)
            if len(absoluteUrls) > 0:
                absoluteUrl = absoluteUrls[0]
                if absoluteUrl != url and absoluteUrl not in urlsFound:

                    # Add it to our results
                    results.append({
                        'url' : absoluteUrl,
                        'preview' : description
                    })
                    urlsFound.append(absoluteUrl)

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

    
    def __buildAbsoluteLinks(self, links, parentUrl):
        """
          Builds a list of absolute links for a given list of relative links and a parent/root url.
        """

        # Create a new list of absolute links
        absoluteLinks = []

        # Get the directory of the old link
        lastForwardSlash = parentUrl.rfind('/')
        parentDirectory = parentUrl[:lastForwardSlash]

        # Rewrite all of the given links to absolute links
        for link in links:

            # Take care of absolute links
            if link.startswith('http'):
                absoluteLinks.append(link)

            # Ignore links linking back to this page
            elif link.startswith('#') or len(link)==0:
                continue

            # Rewrite relative-absolute links
            elif link.startswith('/'):
                link = parentDirectory + link
                absoluteLinks.append(link)

            # Rewrite relative links
            elif not link.startswith('http'):
                link = parentDirectory + '/' + link
                absoluteLinks.append(link)

        # A regular expression for finding 'up' directories
        upDirectoryRegex = re.compile("/.*?/\.\./?")

        # Iterate over the absolute links and clean them up (remove 'up' directory paths)
        cleanAbsoluteLinks = []
        for absoluteLink in absoluteLinks:

            # Pull this out of the list
            cleanAbsoluteLink = absoluteLink

            # Find all occurrences of the 'up' pattern
            occurrences = upDirectoryRegex.findall(cleanAbsoluteLink)

            # Find the location of the right most '/', before the "/../" string, and replace the occurrences with the
            #   rightmost matches
            for occurrence in occurrences:
                if occurrence.count("/")>3:

                    # Find the occurrences of '/--some-folder/../'
                    strippedOccurrence = occurrence.rstrip("/.")
                    indexOfLastSlash = strippedOccurrence.rfind("/")
                    modifiedOccurrence = occurrence[indexOfLastSlash:]

                    # Replace this occurrence with the modified one
                    occurrences.remove(occurrence)
                    occurrences.append(modifiedOccurrence)


            # Keep replacing the occurrences we found until none are left
            while len(occurrences) > 0:

                # Find the location of the right most '/', before the "/../" string, and replace the occurrences with the
                #   rightmost matches
                for occurrence in occurrences:
                    if occurrence.count("/")>3:

                        # Find the occurrences of '/--some-folder/../'
                        strippedOccurrence = occurrence.rstrip("/.")
                        indexOfLastSlash = strippedOccurrence.rfind("/")
                        modifiedOccurrence = occurrence[indexOfLastSlash:]

                        # Replace this occurrence with the modified one
                        occurrences.remove(occurrence)
                        occurrences.append(modifiedOccurrence)

                # Replace each occurrence
                for occurrence in occurrences:
                    cleanAbsoluteLink = cleanAbsoluteLink.replace(occurrence, "/")

                # Find all remaining occurrences of this pattern
                occurrences = upDirectoryRegex.findall(cleanAbsoluteLink)

            # Put this link back in the list
            cleanAbsoluteLinks.append(cleanAbsoluteLink)

        return cleanAbsoluteLinks