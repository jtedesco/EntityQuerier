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

class PageRankExtension(Extension):
    """
      Extension that allows finding the PageRank of a page.
    """

    def __init__(self):
        from util.PRCache import PRCache
        self.prCache = PRCache()

        
    def run(self, resultDictionary):
        resultDictionary['pageRank'] = self.prCache.getPageRank(resultDictionary['url'])

        
def getPageRank(url):
    hsh = __checkHash(__hashUrl(url))
    gurl = 'http://toolbarqueries.google.com/tbr?client=navclient-auto&features=Rank&ch=%s&q=info:%s' % (hsh,urllib.quote(url))
    try:
        f = urllib.urlopen(gurl)
        rank = f.read().strip()[9:]
    except Exception:
        rank = 'N/A'
    if rank == '':
        rank = '0'
    return rank


def __intStr(string, integer, factor):
    for i in range(len(string)) :
        integer *= factor
        integer &= 0xFFFFFFFF
        integer += ord(string[i])
    return integer


def __hashUrl(string):
    c1 = __intStr(string, 0x1505, 0x21)
    c2 = __intStr(string, 0, 0x1003F)

    c1 >>= 2
    c1 = ((c1 >> 4) & 0x3FFFFC0) | (c1 & 0x3F)
    c1 = ((c1 >> 4) & 0x3FFC00) | (c1 & 0x3FF)
    c1 = ((c1 >> 4) & 0x3C000) | (c1 & 0x3FFF)

    t1 = (c1 & 0x3C0) << 4
    t1 |= c1 & 0x3C
    t1 = (t1 << 2) | (c2 & 0xF0F)

    t2 = (c1 & 0xFFFFC000) << 4
    t2 |= c1 & 0x3C00
    t2 = (t2 << 0xA) | (c2 & 0xF0F0000)

    return t1 | t2


def __checkHash(hashInt):
    hash_str = '%u' % hashInt
    flag = 0
    checkByte = 0

    i = len(hash_str) - 1
    while i >= 0:
        byte = int(hash_str[i])
        if 1 == (flag % 2):
            byte *= 2
            byte = byte / 10 + byte % 10
        checkByte += byte
        flag += 1
        i -= 1

    checkByte %= 10
    if 0 != checkByte:
        checkByte = 10 - checkByte
        if 1 == flag % 2:
            if 1 == checkByte % 2:
                checkByte += 9
            checkByte >>= 1

    return '7' + str(checkByte) + hash_str

