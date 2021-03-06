#!/usr/bin/env python

# Test batch job arguments
# This version tests the 'new' ArgumentParser behaviour of IjpOptionParser
# Essentially, just reports whatever it finds on the command line
# usage: test_args options
# (mandatory) options: --sessionId=<sessionId> --icatUrl=<icatUrl> --idsUrl=<idsUrl>
# optional options: --datasetIds=<id1,...> --datafileIds=<id1,...> (though normally at least one would be defined)
# Further options: --option1=<string> --option2=<string>

import sys
import os
import logging

# Use local cat_utils.py - a proper installation would install it as a package
from cat_utils import IjpOptionParser

logging.basicConfig(level=logging.CRITICAL)

usage = "usage: %prog options"

# Turn off old options behaviour in the parser

parser = IjpOptionParser(usage,oldOptionsBehaviour=False)

# Placeholder for any positional arguments
# If the jobscript does any processing of positional arguments, then
# they have to be declared here. 
# This is the simplest form:

parser.add_argument("args",nargs="*",
                help="Positional (non-option) arguments")

# Options specific to this script
# Job Type specs can choose to use these, but can't invent their own
# (parse_args() will throw an error for unknown options)
# NOTE: most options specified here only have a long-form,
# so must always appear on the command-line as --option-name=value or --option-name value,
# even for boolean flags. '--silent --viewtype blah' will set 'silent' to '--viewtype',
# and leave 'blah' as an argument instead of as the value of the viewtype option.
# New scripts should use add_argument rather than add_option;
# a 'reimagining' of add_option is available, but only for
# backwards compatibility with pre-existing usage.

parser.add_option("--option-one", dest="optionOne",
                 help="script-specific option 1")
parser.add_argument("--option-two", dest="optionTwo",
                 help="script-specific option 2")
parser.add_argument("--mode", dest="mode",
                  help="plain, verbose or effusive")
parser.add_argument("--silent", dest="silent",
                  help="keep quiet, regardless of --mode")
parser.add_argument("--viewtype", dest="viewtype",
                  help="View type (fullframe, beads, etc.)")
parser.add_argument("--index", dest="index",
                  help="Initial index (0-10, default 1)")
parser.add_argument("--origin", dest="origin",
                  help="Origin (range [-2.0,2.0]")

# New behaviour will only return a single value;
# We call it options for historical reasons, 
# though it should hold all the arguments

options = parser.parse_args()

jobName = os.path.basename(sys.argv[0])
print jobName, "starting..."

# The 'args' value should hold non-optional arguments

rest = options.args  

# Options we don't want to report on twice,
# including the positional args we declared earlier:
coveredOptions = ['args']

if options.sessionId:
    print "ICAT sessionId provided"
else:
    print "No ICAT sessionId provided"

coveredOptions.append('sessionId')

# Report icat/ids URLs if present

if options.icatUrl:
    print "ICAT url =", options.icatUrl
else:
    print "ICAT url not supplied"

coveredOptions.append('icatUrl')

if options.idsUrl:
    print "IDS url =", options.idsUrl
else:
    print "IDS url not supplied"

coveredOptions.append('idsUrl')

if options.datasetIds:
    print "datasetIds = ", options.datasetIds
else:
    print "datasetIds not supplied"

coveredOptions.append('datasetIds')

if options.datafileIds:
    print "datafileIds = ", options.datafileIds
else:
    print "datafileIds not supplied"

coveredOptions.append('datafileIds')

if options.optionOne:
    print "Option 1 = ", options.optionOne

coveredOptions.append('optionOne')

if options.optionTwo:
    print "Option 2 = ", options.optionTwo

coveredOptions.append('optionTwo')

if options.mode:
    print "Mode = ", options.mode

coveredOptions.append('mode')

if options.silent:
    # Note: print the value of silent; we expect a boolean,
    # but this helps debug misuses such as 'test_args --silent --viewtype whitebeam'
    print "Silent = ", options.silent
else:
    print "Silent = false"
    
coveredOptions.append('silent')

if options.viewtype:
    print "View type = ", options.viewtype
    
coveredOptions.append('viewType')

if options.index:
    print "Index = ", options.index

coveredOptions.append('index')

if options.origin:
    print "Origin = ", options.origin

coveredOptions.append('origin')

# List all other non-empty options
print "Other options (if any):"
for opt, value in options.__dict__.items():
    if value and (opt not in coveredOptions):
        print "  ", opt, "=", value

print "Other command-line arguments (if any): ",
for arg in options.args:
    print arg,
print

print jobName, "completed."
