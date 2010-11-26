#!/usr/bin/env python

from urllib import urlopen
from socket import setdefaulttimeout

from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef
from rdflib.namespace import Namespace

dct = Namespace('http://purl.org/dc/terms/')
g = ConjunctiveGraph('Sleepycat')
g.open('store')
setdefaulttimeout(20)

for s, o in g.subject_objects(predicate=dct['source']):
    try: 
        info = urlopen(o)
        status = info.getcode()
    except Exception, e:
        status = str(e)
    print s, "\t", o, "\t", status

g.close()
