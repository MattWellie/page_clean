"""
Imports the variants which pass the initial 'gene of interest' filtering step
Use these variants (proband, gene, position) to construct zgrep queries
These queries will be used to find the original VCF entries
The VCF entries contain annotations of allele frequencies, which are used in final printout
"""

import sys

in_file = sys.argv[1]  
queries_out = sys.argv[2]
ped = sys.argv[3]
template = 'echo -n -e "{}\t{}\t"; zgrep {} {} | grep {}'

""" 
Can't rely on the template, as each reprocessing of the daya will have a different 
date, meaning that the single template is a flawed strategy

Solve this by making an dictionary of all the file locations by parsing the PED file
"""

ped_dict = {}
with open(ped, 'r') as handle:
    # Parse the PED file, which is in the format [Trio, Proband, Parent1, Parent2, Sex, Affected, File location]
    for line in handle:
        if line == '': pass
        else:
            line_list = line.split('\t')
            assert len(line_list) == 7, exit('Whoa, wrong number of entries in the PED')
            parent1, parent2 = line_list[2:4]
            if parent1 != '0' or parent2 != '0':
                ped_dict[line_list[1].rstrip()] = line_list[6].rstrip() 
                
with open(in_file, 'r') as handle:
    with open(queries_out, 'w') as outhandle:
        for line in handle:
            if '----------' in line: 
                filename = line.split('----------')[1]
                print >>outhandle, 'echo "{}"'.format(filename.rstrip())
            else:
                list = line.split('\t')
                if list[0] == 'proband': continue
                else:
                    PP = list[0]
                    vcf_location = ped_dict[PP]
                    pp1 = PP[2:4]
                    pp2 = PP[4:]
                    pos = list[4]
                    gene = list[5]
                    print >>outhandle, template.format(PP, gene, gene, vcf_location, pos)
