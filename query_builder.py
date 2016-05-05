# Script to build queries based on results from variants passing filters

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
