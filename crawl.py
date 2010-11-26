#!/usr/bin/env python

"""
Crawl the rdfa at data.gov.uk and store them away in a BerkeleyDB triplestore.
"""

import re
import urllib

import rdflib

# set the user agent so that data-gov-uk will know who we are
rdflib.parser.headers = {"User-agent": "data-gov-uk-harvester <https://github.com/edsu/data-gov-uk-harvester>"}

graph = rdflib.ConjunctiveGraph('Sleepycat')
graph.open('store', create=True)

# the paged package listing that we will crawl to discover dataset urls
page_url_tmpl = "http://data.gov.uk/search/apachesolr_search/?filters=type:ckan_package&page=%s"
page = 0

# extract rdf from each dataset html/rdfa page
while True:
    page += 1
    page_url = page_url_tmpl % page
    print "fetching list of datasets from %s" % page_url
    html = urllib.urlopen(page_url).read()

    found = 0
    for dataset_url in re.findall(r'"(http://data.gov.uk/dataset/.*?)"', html):
        found += 1
        print "fetching dataset %s" % dataset_url
        try:
            graph.parse(location=dataset_url, format='rdfa', lax=True)
        except Exception, e:
            print e

    if found == 0:
        break

# no sense in keeping tons of css stylesheet assertions is there?
for t in graph.triples((None, rdflib.URIRef('http://www.w3.org/1999/xhtml/vocab#stylesheet'), None)):
    graph.remove(t)

graph.serialize(open('data.rdf', 'w'))
graph.close()
