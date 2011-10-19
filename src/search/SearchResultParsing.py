from BeautifulSoup import BeautifulSoup
import os
import urllib2
import sys

__author__ = 'jon'

# Spoof the User-Agent so we don't get flagged as spam
SPOOFED_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"

def getPageContent(url):
    """
      Returns the text content of a single URL. (emulates Firefox 7 on Linux for the user-agent)

        @param  url The url from which to fetch the content
        @return The contents of the page
    """

    # Find where we expect this data to be cached
    cachePath = str(os.getcwd())
    cachePath = cachePath[:cachePath.find('EntityQuerier') + len('EntityQuerier')]
    cachePath += '/cache/' + url.replace('/', '')

    if os.path.exists(cachePath) and os.path.isfile(cachePath):

        content = open(cachePath).read()

    else:

        # Build a request object to grab the content of the url
        request = urllib2.Request(url)
        request.add_header("User-Agent", SPOOFED_USER_AGENT)

        # Open the URL and read the content
        opener = urllib2.build_opener()
        content = opener.open(request).read()

        # Try to cache the result
        try:
            
            cache = open(cachePath, 'w')
            cache.write(content)
            cache.close()

        except IOError:

            # This frequently happens when the URL is too long to act as a filename
            pass

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


def isHTML(content):
    """
      Check whether or not some content is HTML
    """

    return '<html' in content or 'html>' in content