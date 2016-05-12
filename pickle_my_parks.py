"""   
This script will find files prefixed with 'park_', which contain gene lists from Park 2008 (Analysis of human disease genes in the context of gene essentiality)
http://dx.doi.org/10.1016/j.ygeno.2008.08.001
 - These lists were manually copied into text files named in the format 'park_phenotype_association.txt'
 - The phenotype isolated from the title will be used as a dictionary key for the genes it contains

The dictionary will be pickled as 'pickled_park.cPickle'
"""

import cPickle, os

# List comprehension to identifiy text files of interest
# Any other text files could be caught if prefixed with park_ to expand the search
files = [file for file in os.listdir('.') if file.split('_')[0] == 'park']
outdict = {}

for file in files:
    with open(file, 'r') as handle:
        # Grab the phenotype as a name by removing 'park_' and '.txt'
        phenotype = ('_').join(file.split('.')[0].split('_')[1:])
        print phenotype
        # Create a set rather than a list in case of non-uniques
        outdict[phenotype] = set()
        for gene in handle:
            gene=gene.rstrip()
            outdict[phenotype].add(gene)

with open('pickled_park.cPickle', 'wb') as handle:
    cPickle.dump(outdict, handle)
