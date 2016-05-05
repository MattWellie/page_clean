#!/bin/bash
# Does this need to be a shell script? Not really.. The whole thing could have been done as a single python or perl program but i fancied trying out something new.

# This will run the whole intersect of variants exported from the clinical filtering process against the genes identified as mouse related, so long as 'genes_of_interest.cPickle' and 'pickled_parks.cPickle' are present (or the appt. options are set to allow it to run from a batch IMPC query in TSV form, and 'park_' prefixed text files

for i in "$@"
    do
    case $i in
        # The file containing the results of the impc batch query
        -f=*|--filein=*)
        impc="${i#*=}"
        ;;
        
        # The file containing the results of the clinical filtering script
        -c=*|--clinicalfilter=*)
        clin="${i#*=}"
        ;;
        
        # This will be 1 if you have parks gene list files to condense, otherwise this is skipped
        -p=*|--parks=*)
        parks="${i#*=}"
        ;;

        # The intersection of the gene lists with the clinical filtering output
        -filter=*)
        filterout="${i#*=}"
        ;;

        # The name of a Bash script which will be written to query the original VCFs
        -q=*|--query=*)
        query="${i#*=}"
        ;;
        
        # The name of a file which will be used to contain the zgrep results from database
        -qr=*)
        queryresults="${i#*=}"
        ;;
        
    esac
done

# Run this to check if the file containing the impc batch results is there
# Default action is ignore this command
if [ -f "$impc" ]
then
    python batch_process.py -filein $impc
fi

# If the parks argument is 1
if [ "$parks" = "1" ]
then
    python pickle_my_parks.py
fi

# To tidy up all that mess... Convert pickles to text lists
# This can be run whether the previous steps were run or not
# Makes the final outputs available to perl or python
python pickle_to_genelist.py

# At this point you should have run the clinical filtering script on an appropriate cohort... The name of that output file should be the argument -filter -> $filterout

# This step scans the clinical filtering output against the lists of gene names
# This will be a text file delimited by lines of '----------filename.txt' identifying which results correspond to which gene lists. This will later be re-referenced against the park file, so may be redundant
python python_scan.py $clin genelist_* > $filterout

# Based on the output of the intersection script, this will build queries on the original VCFs
# From the lines which passed clinical filtering, construct zgrep queries to get full annotation
python query_builder.py  $filterout  $query

# Run that shell script, sending all outcomes of the zgrep commands to a text file (arg)
bash $query > $queryresults

# Run a script to pair up all variants passing filter with their allele freqs
python freq_writer.py $queryresults
rm genelist_*
