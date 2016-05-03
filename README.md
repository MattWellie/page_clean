# page_clean

This is a minimal version of the PAGE_MPO folder, integrating both the Park gene list and the lists obtained through querying the IMPC database

The entire process can be operated through use of the bash_control script

-- -f/--filein : a .TSV file containing the results of the IMPC batch query (optional)

-- -c/--clinicalfilter : a file containing the output of the clinical filtering script run on an appropriate trio (Jeremy McRae)

-- -p/--parks : 1 as an argument will condense separate park gene lists (a workaround. Will collect and pickle files named park_*)

-filter : The intersection of the genelists with the clinical filtering output

-q/--query : the name of a Bash script which will be written. Might be best to provide a default value here... it's not important 

-qr : Name of a file to contain the zgrep results.. Again it might be best to have this default to something sensible
