# page_clean

This is a minimal version of the PAGE_MPO folder, integrating both the Park gene list and the lists obtained through querying the IMPC database

The entire process can be operated through use of the bash_control script

* -f/--filein : a .TSV file containing the results of the IMPC batch query (optional)
* -c/--clinicalfilter : a file containing the output of the clinical filtering script run on an appropriate trio (Jeremy McRae)
* -p/--parks : 1 as an argument will condense separate park gene lists (a workaround. Will collect and pickle files named park_*)
* -filter : The intersection of the genelists with the clinical filtering output
* -q/--query : the name of a Bash script which will be written. Might be best to provide a default value here... it's not important
* -qr : Name of a file to contain the zgrep results.. Again it might be best to have this default to something sensible

1. batch_process.py - This is a script to take the 'batch query' results from the IMPC web resource and process them into a single file; genes_of_interest.cPickle
2. pickle_my_parks.py - This takes the TSV files from the supplementary information section of Analysis of human disease genes in the context of gene essentiality, Park et al., and convert them into something usable. This is a two-(or more)-part fix due to the need to transfer them to and from Gen1 to operate on the VCF files. This script opens each category of the Park data and stores each in a single pickled file. All these files have to be prefixed with "park_"
3. pickle_to_genelist.py - After pickling the objects, they are much easier to transfer across/are saved for git, so this script can unpack them again. This separates the gene lists into separate lists by category, with each file prefixed with "genelist_"
4. python_scan.py - Parses the 'VCF' file exported by the clinical filtering script, to store the contents in a dictionary. The indices of the dict are the genes implicated in each variant, the list under those indexes stores each row with that gene implicated. This is then cross referenced against those gene lists, to print the annotations which correspond to the genes in each file
5. query_builder.py - Using a template grep search command, this script processes each one of the variants identified from the clinical filtering script and creates a search for the corresponding row in the original VCF file (with the full annotations). These are written to a shell script file
The shell file containing all the grep queries is executed and redirected to a text file for the results
6. match.py - This script takes the variants from the grep output, matched them up with the variant rows from the clinical filtering, and uses the allele frequencies, chromosomal position, and patient ID to print out a short summary for each patient. Might need reworking, some variants appear to go missing.

