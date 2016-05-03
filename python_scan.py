"""
A python version of the perl scan file
As the VCF is being parsed as .txt, Perl isn't mega useful so I'm back to py
"""

import os, sys

# This is the VCF file of results passed via clinical filtering script
input_file = sys.argv[1]
# The gene files will all  be text, one gene symbol per line
gene_files = sys.argv[2:]

vcf_gene_dict = {}

with open(input_file, 'r') as handle:
    first_line = True
    for row in handle:
        if first_line:
            first_line = False
        else:
            genes = row.split('\t')[5].split(',')
            for gene in genes:
                if gene in vcf_gene_dict:
                    vcf_gene_dict[gene].add(row)
                else:
                    vcf_gene_dict[gene] = set([(row)])

for file in gene_files:
    with open(file, 'r') as handle:
        print '----------{}'.format(file)
        for gene in handle:
            gene = gene.rstrip()
            if gene in vcf_gene_dict:
                for row in vcf_gene_dict[gene]:
                    print row.rstrip()

