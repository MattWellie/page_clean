"""
This script builds queries on the original VCF files, based on the varaints picked up by intersection with disease gene lists
The template query specified up top has been used as the accurate file location as of 06/05/2016

The queries constructed use zgrep (vcf files are gzipped) for the gene name, then piped to a second grep for the variant position 
As the VCF file is implicitly located based on the PP#### ID, the gene and positional ID are enough to uniquely ID the row
The return from this is prefixed with the PP# ID and gene name, tab-separated, to prevent the need to re-query the files later
    (The original process was to obtain these VCF rows, then parse all results which passed the filter to match these back up with PP IDs... dumb)
This was expected to be easier than parsing each line of each VCF file manually, but can run a little slow doe to file sizes

-- If changes are made to the location of the original VCF files, this template query will need to be changed. It is possible to make something simila

"""

import sys

in_file = sys.argv[1]  
queries_out = sys.argv[2]
template = 'echo -n -e "{}\t{}\t"; zgrep {} /lustre/scratch115/realdata/mdt3/projects/pagedata/data_freezes/2015-09-03/PP/{}/{}/{}/vcf/{}.uber_vep_tabix_qc.2015-11-11.vcf.gz | grep {}'

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
                    pp1 = PP[2:4]
                    pp2 = PP[4:]
                    pos = list[4]
                    gene = list[5]
                    print >>outhandle, template.format(PP, gene, gene, pp1, pp2, PP, PP, pos)
