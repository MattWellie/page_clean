import cPickle

"""
Hack to get names out of a cPickle serialised object saved as a text file

This will read in genes_of_interest, and all of the Park gene sets
Each of these will be written out as a separate text file list
The files will have a name starting 'genelist_'

There will be a file written out containing the names of all these individual files
There will also be a single file containing all the unique gene names across all files
This will be called 'all_genes.txt'
"""

# Set input names:
interesting = 'genes_of_interest.cPickle' # A python set()
parks = 'pickled_parks.cPickle'
filenames = set()
filenames_out = 'gene_list_files.txt'
all_genes = set()

with open(interesting, 'r') as handle:
    gene_set = cPickle.load(handle)
    with open('genelist_impc.txt', 'w') as outhandle:
        filenames.add('genelist_impc.txt')
        for gene in gene_set:
            all_genes.add(gene)
            print >>outhandle, gene

with open(parks, 'r') as handle:
    park_dict = cPickle.load(handle)
    for phenotype in park_dict:
        gene_set = park_dict[phenotype]
        with open('genelist_{}.txt'.format(phenotype), 'w') as outhandle:
            filenames.add('genelist_{}.txt'.format(phenotype))  
            for gene in gene_set:
                all_genes.add(gene)
                print >>outhandle, gene

with open(filenames_out, 'w') as filehandle:
    for filename in filenames:
        print >>filehandle, filename
        
with open('all_genes.txt', 'w') as handle:
    for gene in all_genes:
        print >>handle, gene
