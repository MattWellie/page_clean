"""   
This script will find files prefixed with 'park_', which contain gene lists from Park 2008   
The gene lists will then be read into a dictionary, indexed by their file name

The dictionary will be pickled as 'pickled_park.cPickle' (not park prefixed to 
prevent some future errors)
"""

import cPickle, os

files = [file for file in os.listdir('.') if file.split('_')[0] == 'park']

outdict = {}

for file in files:
    with open(file, 'r') as handle:
        phenotype = ('_').join(file.split('.')[0].split('_')[1:])
        print phenotype
        outdict[phenotype] = set()
        for gene in handle:
            gene=gene.rstrip()
            outdict[phenotype].add(gene)

with open('pickled_park.cPickle', 'wb') as handle:
    cPickle.dump(outdict, handle)
