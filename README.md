# page_clean

This is a minimal version of the PAGE_MPO folder, integrating both the Park gene list and the lists obtained through querying the IMPC database

The entire process can be operated through use of the bash_control script

* -p/--ped : Name of the PED file used to locate VCF files for the probands. If the clinical filtering variable is set to 1, this file will also be used to kick off the clinical filtering script (this will take a while)
* -f/--filein : a .TSV file containing the results of an IMPC batch query (optional)
* -r/--runclin : 1 as an argument will kick off the naive (no file filters) clinical filtering process. Reqiures the PED and clinical filter file names to be set. The clinical filter argument can/should be a new file, as it will be created during the process.
* -c/--clinicalfilter : a file containing the output of the clinical filtering script run on an appropriate trio, or set of trios (https://github.com/jeremymcrae/clinical-filter). If the clinical filtering 
* -p/--parks : 1 as an argument will condense separate park gene lists (a workaround. Will collect and pickle files named park_*, also optional)
* -filter : The intersection of the genelists with the clinical filtering output
* -q/--query : the name of a Bash script which will be written. Might be best to provide a default value here... it's not important
* -qr : Name of a file to contain the zgrep results.. Again it might be best to have this default to something sensible


1. The clinical filtering script will be kicked off, using the ped file and output name specified (only runs if the -r argument is 1, pre-processed output can also be supplied)
2. batch_process.py - This is a script to take the 'batch query' results from the IMPC web resource and process them into a single file; genes_of_interest.cPickle
2. pickle_my_parks.py - This takes the TSV files from the supplementary information section of Analysis of human disease genes in the context of gene essentiality, Park et al., and convert them into something usable. This is a two-(or more)-part fix due to the need to transfer them to and from Gen1 to operate on the VCF files. This script opens each category of the Park data and stores each in a single pickled file. All target files are prefixed with "park_". The file titles either include 'nondisease', or are associated with a human disease phenotype
3. pickle_to_genelist.py - After pickling the objects, they are much easier to transfer across/are saved for git, so this script can unpack them again. This separates the gene lists into separate lists by category, with each file prefixed with "genelist_"
4. python_scan.py - Parses the 'VCF' file exported by the clinical filtering script, to store the contents in a dictionary. The indices of the dict are the genes implicated in each variant, the list under those indexes stores each row with that gene implicated. This is then cross referenced against those gene lists, to print the annotations which correspond to the genes in each file
5. query_builder.py - Parses the PED file used to run the clinical filtering process, identifies all probands and stores their VCF file locations. This script then processes each one of the variants identified from the clinical filtering script and creates a zgrep search command for the corresponding row in the original VCF file (with the full annotations). These are written to a shell script file.
The shell file containing all the grep queries is executed and redirected to a text file for the results. Parsing the PED file at this point would also allow for the identification of probands which are sequenced as part of an incomplete trio.
6. freq_writer.py - This script takes the variants from the grep output, matched them up with the variant rows from the clinical filtering, and uses the allele frequencies, chromosomal position, and patient ID to print out a short summary for each patient. Might need reworking, some variants appear to go missing.

Example usage:
To run the process on pre-filtered data
$ bash bash_control.sh -c=pilot_filtered.txt -filter=filteredfilter.txt -q=query.sh -qr=zgrep_results.txt -p=df2ped.txt

To run the process including execution of the clinical filtering process
$ bash bash_control.sh -r=1 -c=pilot_filtered.txt -filter=filteredfilter.txt -q=query.sh -qr=zgrep_results.txt -p=df2ped.txt

**Things that might be useful to know:

Minimum file set required: clinical filtering output, the PED file used to identify the VCFs for that process, genes_of_interest.cPickle, pickled_parks.cPickle
the cPickle files can be recreated from the base input, but the first two commands in bash_control are optional

The input from the clinical filtering process is in a tab-delimited arrangement: [proband	alternate_ID	sex	chrom	position	gene	mutation_ID	transcript	consequence	ref/alt_alleles	MAX_MAF	inheritance	trio_genotype	mom_aff	dad_aff	result	pp_dnm	exac_allele_count]
From this file, this script process explicitly uses columns 0, 3, 4, 5 (PPID, chromosome, position, gene name)

Additional features such as Ref/Alt and allele frequencies are later grabbed from the VCF where appropriate

## TODO
Maybe include a way of indicating any variants which are present on the DDG2P, to rule out or flag them. 

Incorporate haploinsufficiency scores where available

Change the output format to a TSV file, of arbitrary column length depending on number of annotations

Change Bash script so some intermediate files have default values (e.g. the zgrep queries)
