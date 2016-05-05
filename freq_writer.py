"""
Reworked script which taked in the file of zgrep query results and processes them
into a final output file
"""
import re, sys, cPickle

# Compile the RegEx string to search for allele frequencies
allele_freq = re.compile(";(?P<AF>[A-Z_35]*?_AF)=(?P<value>0\..*?);")

# Import the zgrep results file name from CMD
grep_in = sys.argv[1] # Grep results
detail_dict = {}

# Open the Park pickled object to identify gene names
with open('pickled_parks.cPickle', 'r') as handle:
    pickled_parks = cPickle.load(handle)

# Let's begin..
with open(grep_in, 'r') as handle:
    for line in handle:
        try:
            line_list = line.split('\t')
            PP = line_list[0]
            gene = line_list[1]
            chrom = line_list[2]
            pos = line_list[3]
            ref = line_list[5]
            alt = line_list[6]
            
            # Get allele frequencies using regex defined above
            AF = []
            groups = re.findall(allele_freq, line)
            if len(groups) >= 1:
                for group in groups:
                    AF.append('{} = {}'.format(group[0], group[1]))
            else:
                AF=[('No AF data')]
                
            if PP not in detail_dict: detail_dict[PP] = {}
            detail_dict[PP][chrom+pos] = {'gene': gene,
                                          'chrom': chrom,
                                          'pos': pos,
                                          'ref': ref,
                                          'alt': alt,
                                          'af': AF}
        except:
            print 'I don\'t like this line: {}'.format(line)

# Now print this summary to an output file
with open('allele_freqs.txt', 'w') as handle:
    print >>handle, 'PP IDs, variants, and corresponding allele freqs'
    for PP in detail_dict:
        print >>handle, '\n{}'.format(PP)
        cp_keys = sorted(detail_dict[PP].keys())
        for key in cp_keys:
            gene = detail_dict[PP][key]['gene']
            chrom = detail_dict[PP][key]['chrom']
            pos = detail_dict[PP][key]['pos']
            ref = detail_dict[PP][key]['ref']
            alt = detail_dict[PP][key]['alt']
            af = detail_dict[PP][key]['af']
            
            park = ''
            park_tf = False
            for phenotype in pickled_parks:
                if gene in pickled_parks[phenotype]:
                    park_tf = True
                    park = ' '.join(phenotype.split('_'))
            if park_tf:
                print >>handle, '\t{}: {} {}>{} - {}\t(Park: {})'.format(chrom, pos,\
                                                                         ref, alt,\
                                                                         gene, park)
            else:
                print >>handle, '\t{}: {} {}>{} - {}'.format(chrom, pos, ref, alt, gene)
            for afreq in af:
                print >>handle, '\t\t{}'.format(afreq)
        
