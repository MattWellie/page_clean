import cPickle

"""
Hack to get names out of a cPickle serialised object saved as a text file
This pickle file is created in pickle_my_parks, and may not be necessary in future ( i was being lazy..)
The genes_of_interest.cPickle file is created in batch_process.py
It would be pretty trivial to merge pickle_my_parks and batch_process, ICBA

This will read in genes_of_interest, and all of the Park gene sets
There is no real reason for 'gene_of_interest' and park etc. not already abing in the same file
Each of these will be written out as a separate text file list
The files will have a name starting 'genelist_'

There will be a file written out containing the names of all these individual files
There will also be a single file containing all the unique gene names across all files
This will be called 'all_genes.txt'
"""

# Set input names:
interesting = 'genes_of_interest.cPickle' # A python set()
parks = 'pickled_parks.cPickle'

# Create a variable for holding all the gene file names (may be useful to keep a record)
filenames = set()
filenames_out = 'gene_list_files.txt'

# Start a set to record all gene names across all sets (might be useful for searching for any matches when debugging, or using grep to query the whole set in one location)

all_genes = set()

# Extract the contents from the gene_of_interest first
# Write to 'genelist_impc.txt': International Mouse Phenotyping Consortium
with open(interesting, 'r') as handle:
    gene_set = cPickle.load(handle)
    with open('genelist_impc.txt', 'w') as outhandle:
        filenames.add('genelist_impc.txt')
        for gene in gene_set:
            all_genes.add(gene)
            print >>outhandle, gene

# Open the pickled_parks file and read ecah phenotype association into a separate list object
# These files will be named genelist_<phenotype>.txt
with open(parks, 'r') as handle:
    park_dict = cPickle.load(handle)
    for phenotype in park_dict:
        gene_set = park_dict[phenotype]
        with open('genelist_{}.txt'.format(phenotype), 'w') as outhandle:
            filenames.add('genelist_{}.txt'.format(phenotype))  
            for gene in gene_set:
                all_genes.add(gene)
                print >>outhandle, gene

# Export the collection of filenames generated so far
with open(filenames_out, 'w') as filehandle:
    for filename in filenames:
        print >>filehandle, filename
        
# Export the list of all gene names seen so far        
with open('all_genes.txt', 'w') as handle:
    for gene in all_genes:
        print >>handle, gene
