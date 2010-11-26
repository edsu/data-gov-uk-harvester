#!/usr/bin/env python

from rdflib.graph import ConjunctiveGraph
from rdflib.namespace import Namespace

dct = Namespace('http://purl.org/dc/terms/')

g = ConjunctiveGraph('Sleepycat')
g.open('store')

subjects = {}
for o in g.objects(predicate=dct['subject']):
    sub = o.split('/')[-1]
    subjects[sub] = subjects.get(sub, 0) + 1

sorted_keys = subjects.keys()
sorted_keys.sort(lambda a, b: cmp(subjects[b], subjects[a]))

for subject in sorted_keys:
    print subject, "\t", subjects[subject]
