#!/usr/bin/env python
#
#  Script for getting Google Page Rank of page
#  Google Toolbar 3.0.x/4.0.x Pagerank Checksum Algorithm
#
#  original from http://pagerank.gamesaga.net/
#  this version was adapted from http://www.djangosnippets.org/snippets/221/
#  by Corey Goldberg - 2010
#
#  Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

import urllib
from src.search.extension.Extension import Extension
from src.util.PageRankUtility import checkHash, hashUrl

class PageRankExtension(Extension):
    """
      Extension that allows finding the PageRank of a page.
    """

    def __init__(self):
        from src.cache.PRCache import PRCache
        self.prCache = PRCache()


    def run(self, resultDictionary):
        resultDictionary['pageRank'] = getPageRank(resultDictionary['url'])


def getPageRank(url):
    hsh = checkHash(hashUrl(url))
    gurl = 'http://toolbarqueries.google.com/tbr?client=navclient-auto&features=Rank&ch=%s&q=info:%s' % (hsh,urllib.quote(url))
    try:
        f = urllib.urlopen(gurl)
        rank = f.read().strip()[9:]
    except Exception:
        rank = 'N/A'
    if rank == '':
        rank = '0'
    return rank