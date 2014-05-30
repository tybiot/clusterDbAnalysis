#!/usr/bin/env python

# This is a pipe command
#
# Pipe in a run ID (or list of run IDs) and it returns to you a 2-column table containing
# the run ID(s) in the first column and all of the cluster IDs contained within it in the second
# column (and gene IDs in the third column)
#
# Results are printed to stdout.

import fileinput, sqlite3, optparse, os
from FileLocator import *

header = [ "runid", "clusterid", "geneid" ]

usage="""%prog [options] < run_ids > cluster_runs

Output: """ + " ".join(header)
description="Given a set of run IDs (from stdin), returns all cluster IDs associated with that run ID"
parser = optparse.OptionParser(usage=usage, description=description)
parser.add_option("-r", "--runcol", help="Column number for run ID (start from 1, D=1)", action="store", type="int", dest="rc", default=1)
parser.add_option("--header", help="Specify to add header to the output file (useful if you want to take the results and put into Excel or similar programs)",
                  action="store_true", default=False)
(options, args) = parser.parse_args()

rc = options.rc - 1

con = sqlite3.connect(locateDatabase())
cur = con.cursor()

if options.header:
    print "\t".join(header)
for line in fileinput.input("-"):
    spl = line.strip('\r\n').split("\t")
    runid = spl[rc]
    query = "SELECT * FROM clusters WHERE clusters.runid = ?;"
    cur.execute(query, (runid, ) )
    
    for l in cur:
        s = list(l)
        stri = "\t".join(str(t) for t in s)
        print stri

con.close()
