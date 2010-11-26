#!/usr/bin/env python

"""
Crawl the rdfa at data.gov.uk and store them away in a BerkeleyDB triplestore.
"""

import re
import urllib

from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef

graph = ConjunctiveGraph('Sleepycat')
graph.open('store', create=True)

page_url_tmpl = "http://data.gov.uk/search/apachesolr_search/?filters=type:ckan_package&page=%s"
page = 0

while True:
    page += 1
    page_url = page_url_tmpl % page
    print "fetching list of datasets from %s" % page_url
    html = urllib.urlopen(page_url).read()

    found = 0
    for dataset_url in re.findall(r'"(http://data.gov.uk/dataset/.*?)"', html):
        found += 1
        print "fetching dataset %s" % dataset_url
        graph.parse(location=dataset_url, format='rdfa', lax=True)

    if found == 0:
        break

# no sense in keeping tons of css stylesheet assertions is there?
for t in graph.triples((None, URIRef('http://www.w3.org/1999/xhtml/vocab#stylesheet'), None)):
    graph.remove(t)

graph.serialize(open('data.rdf', 'w'))
graph.close()
