# Scratchy script to rematch all the variants I can find in the VCFs with the
# corresponding PP numbers, and peel out all the annotations present
import re, sys

allele_freq = re.compile(";(?P<AF>[A-Z_35]*?_AF)=(?P<value>0\..*?);")

filtered_in = sys.argv[1] #'filtered_variant_results.txt'
details_in = sys.argv[2] #'pilot_out.txt'


detail_dict = {}

# Create an index to get at the PP#### values using positions
with open(details_in, 'r') as handle:
    for line in handle:
        list = line.split('\t')
        if list[0] == 'proband': continue
        else:
            PP = list[0]
            pos = list[4]
            chrom = list[3]
            gene = list[5]
            detail_dict['{}:{}'.format(chrom, pos)] = {'pp': PP,
                                                       'gene': gene}
            
allele_freqs = {}
with open(filtered_in, 'r') as handle:
    for line in handle:
        if 'genelist_' in line: continue
        list = line.split('\t')
        # Get PP#### details
        chrom = list[0]
        pos = list[1]
        chrompos = '{}:{}'.format(chrom, pos)
        PP = detail_dict[chrompos]['pp']
        gene = detail_dict[chrompos]['gene']
        
        # Get allele frequencies
        groups = re.findall(allele_freq, line)
        if len(groups) >= 1:
            if PP not in allele_freqs: 
                allele_freqs[PP]={}
            allele_freqs[PP][chrompos] = {'gene': gene,
                                          'afs': []}
            for group in groups:
                allele_freqs[PP][chrompos]['afs'].append('{} = {}'.format(group[0], group[1]))

with open('allele_freqs.txt', 'w') as handle:
    print >>handle, 'PP IDs, variants, and corresponding allele freqs\n'
    for PP in allele_freqs:
        print >>handle, '\n{}'.format(PP)
        for chrompos in allele_freqs[PP]:
            gene = allele_freqs[PP][chrompos]['gene']
            print >>handle, '\t{} - {}'.format(chrompos, gene)
            for af in allele_freqs[PP][chrompos]['afs']:
                print >>handle, '\t\t{}'.format(af)
