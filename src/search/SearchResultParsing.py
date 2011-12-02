import urllib2
from BeautifulSoup import BeautifulSoup
from _socket import setdefaulttimeout
from time import sleep
from urllib2 import HTTPError
import sys
import webbrowser
from util.Cache import Cache

__author__ = 'jon'

# Spoof the User-Agent so we don't get flagged as spam
SPOOFED_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/6.3.1"

# Set a 5 second timeout for all pages
timeout = 5
setdefaulttimeout(timeout)


def loadFromUrl(url):

    # Build a request object to grab the content of the url
    request = urllib2.Request(url)
    request.add_header("User-Agent", SPOOFED_USER_AGENT)

    # Open the URL and read the content
    opener = urllib2.build_opener()
    openSocket = opener.open(request)
    content = openSocket.read()
    openSocket.close()

    return content


def getPageContent(url):
    """
      Returns the text content of a single URL.

        @param  url The url from which to fetch the content
        @return The contents of the page
    """

    # Try to retrieve this url from the cache
    cache = Cache()
    cachedContent = cache.read(url)

    if cachedContent is not None:

        # Take the cached content
        content = cachedContent

    else:

        try:
            # Load the content from the web
            content = loadFromUrl(url)

            # Cache this page
            cache.write(url, content)

        except HTTPError, e:

            print "Encountered HTTP error '%s'" % str(sys.exc_info()[1])
            webbrowser.open(e.url)
            sys.exit(1)

    return content


def parseMetaDataFromContent(content):
    """
      Parses the raw string data from the website. This function acts as a critical helper function to extract the
       title, keywords, and links using regular expressions.

       @param  content the raw content to parse
            title:       should always be able to find
            keywords:    a list, empty if none were found
            description: the meta description of the page or <code>None</code> if none was found
    """

    # Parse this HTML content using 'beautiful soup'
    soup = BeautifulSoup(content)

    # Pull out the title via BeautifulSoup
    try:
        title = soup.find('title').text.encode('ascii', 'ignore').strip('\n').lower()
    except Exception:
        title = ''

    # Pull out the meta data using beautiful soup
    try:
        keywordResults = soup.findAll(attrs={"name":"keywords"})
        keywords = str(keywordResults[0].attrs[0][1]).lower().split(',')
        if len(keywords) == 0 or 'keywords' in keywords:
            keywords = str(keywordResults[0].attrs[1][1]).lower().split(',')
    except Exception:
        keywords = []
    try:
        descriptionResults = soup.findAll(attrs={"name":"description"})
        description = str(descriptionResults[0].attrs[1][1]).lower()
        if len(description) == 0 or 'description' in description:
            description = str(descriptionResults[0].attrs[0][1]).lower()
    except Exception:
        description = ''

    # Return the parsed data
    return title, keywords, description


def parseHeaderInformationFromContent(content):
    """
      Parses text from all header tags, and returns

        @param  content The HTML content to parse
        @return The list of header text
    """

    # Parse this HTML content using 'beautiful soup'
    soup = BeautifulSoup(content)

    # Find all header blocks
    headersTags = []
    headersTags.extend(soup.findAll('h1'))
    headersTags.extend(soup.findAll('h2'))
    headersTags.extend(soup.findAll('h3'))
    headersTags.extend(soup.findAll('h4'))
    headersTags.extend(soup.findAll('h5'))

    # Get the text
    headerText = []
    for headerTag in headersTags:
        headerText.append(headerTag.text.encode('ascii', 'ignore').strip('\n').lower())

    return headerText


def isHTML(content):
    """
      Check whether or not some content is HTML
    """

    return '<html' in content or 'html>' in content
