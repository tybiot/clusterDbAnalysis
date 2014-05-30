#!/usr/bin/env python

# This is NOT a pipe command.
#
# Given one (or multiple to string with ORs) annotation,
# returns all genes in the database matching that annotation.

import optparse, sqlite3, sys
from FileLocator import *
from ClusterFuncs import *

header = [ 'Gene_id', 'Annotation' ]

usage = """%prog \"Annotation 1\" \"Annotation 2\" ... > [Gene_id_list]

Output: """ + " ".join(header)

description = """Get a list of genes in the database matching at least
one of the specified annotations (Note - does not have to match ALL of them)"""

parser = optparse.OptionParser(usage=usage, description=description)
parser.add_option("--header", help="Specify to add header to the output file (useful if you want to take the results and put into Excel or similar programs)",
                  action="store_true", default=False)
(options, args) = parser.parse_args()

if len(args) == 0:
    sys.stderr.write("ERROR: Must provide at least one annotation to match in db_getGenesWithAnnotation.py\n")
    exit(2)

# Change the annotations so that they are all LIKE %name%
teststr = tuple('%' + s + '%' for s in args)

con = sqlite3.connect(locateDatabase())
cur = con.cursor()

query = """SELECT processed.geneid, processed.annotation
           FROM processed
           WHERE ("""

for i in range(len(teststr)):
    query = query + "processed.annotation LIKE ? "
    if not i == len(teststr) - 1:
        query = query + "OR "
query = query + ");"

cur.execute(query, teststr)

if options.header:
    print "\t".join(header)
for l in cur:
    s = list(l)
    stri = "\t".join(str(t) for t in s)
    print stri

con.close()
