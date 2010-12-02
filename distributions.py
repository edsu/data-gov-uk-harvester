#!/usr/bin/env python

import sys
import socket
import httplib
import urllib2
import traceback

import rdflib

dcat = rdflib.Namespace('http://vocab.deri.ie/dcat#')
g = rdflib.ConjunctiveGraph('Sleepycat')
g.open('store')

socket.setdefaulttimeout(20)
for dataset, distribution in g.subject_objects(predicate=dcat.distribution):

    info = None
    try: 
        info = urllib2.urlopen(distribution.encode('utf-8'))
        status = str(info.getcode())
        content_type = info.headers.get('content-type', "")
    except urllib2.HTTPError, e:
        status = str(e.getcode())
        content_type = e.headers.get('content-type', "")
    except urllib2.URLError, e:
        status = "bad url"
        content_type = ""
    except httplib.InvalidURL, e:
        status = e
        content_type = ""

    print "\t".join([dataset, distribution, status, content_type]).encode('utf-8')

g.close()
