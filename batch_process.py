"""
Script to read and split the results from the IMPC batch results files
This takes a TSV file and opens it as a dictionary, continuing to process and export the results
The batch query function of the IMPC website allows for results to be exported in TSV or xlsx

The format of this TSV file is expected to be, tab separated:
<column name> - <contents>

mp_id             - MP:000000, mouse phenotype term
id_link           - URL, not used
mp_term           - text description of term
mp_definition     - more detailed text explanation
mgi_accession_id  - MGI:0000000(|MGI:000001), not used
marker_symbol     - Mouse1(|Mouse2), list of mouse genes associated with mp_id
human_gene_symbol - HUMAN1(|HUMAN2), list of the human orthologues

It is able to run a comparison of the list with DDG2P after parsing, showing overlap etc. This can be used by specifying the 
-ddg2p flag as any value other than 0 (default). If this is not set the files will be parsed and the output file written, 
followed by prematurely quitting
"""

import csv, argparse, cPickle

parser = argparse.ArgumentParser()

parser.add_argument('-filein')
parser.add_argument('-ddg2p', default=0)
args = parser.parse_args()

ddg2p = 'DDG2P.csv'
phenotype_col = 'mp_id'
human_col = 'human_gene_symbol'
mouse_col = 'marker_symbol'
results_dict = {}
all_genes = set()
count = 0

# Open the file as a handle, and then use the csv.DictReader to open it with headings as keys
with open(args.filein, 'r') as handle:
    dict = csv.DictReader(handle, delimiter='\t')
    for row in dict:
        human_set = set()
        phenotype = row[phenotype_col]

        # Get the human gene row, split and count        
        roi = row[human_col]
        separated = roi.split('|')
        for x in separated:
            human_set.add(x)
            all_genes.add(x)
            count += 1
        
        results_dict[phenotype] = {'human_set': human_set,
                                   'human_len': len(human_set)}

# Dump the gene set to a pickle file
with open('genes_of_interest.cPickle', 'w') as handle:
    cPickle.dump(all_genes, handle)

# Allow for premature exit if DDG2P overlap is not important
if args.ddg2p == 0:
	exit()

# Output counts of the genes processed
print 'Unique total: {}'.format(len(all_genes))
print 'Absolute total: {}'.format(count)

# Grab all the gene names from the DDG2P input file
ddg2p_set = set()
first_line = True
with open(ddg2p, 'r') as handle:
    for line in handle: 
        if first_line:
            first_line = False
        else:
            ddg2p_set.add(line.split(',')[0])
		    
print 'Number of DDG2P genes: {}'.format(len(ddg2p_set))            

# And identify how many overlap with the DDG2P gene set
for phenotype in results_dict:
    overlap = 0
    for gene in ddg2p_set:
        if gene in results_dict[phenotype]['human_set']:
            print '{}-Human and DDG2P: {}'.format(phenotype, gene)
            overlap += 1            
    # Total overlapping with each clinical phenotype:
    print 'DDG2P overlap with {}: {}'.format(phenotype, overlap)
