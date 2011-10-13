import sys
from twill.commands import go, formclear, fv, submit, show
if __name__ == '__main__':

    url = sys.argv[1]
    print "Checking PageRank of '%s'" % url

    go('http://nfriedly.com/pagerank')
    formclear('1')
    fv('1', 'q', url)
    submit('2')

    print "==DATA=="
    show()
