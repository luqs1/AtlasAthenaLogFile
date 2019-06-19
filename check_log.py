import re
import argparse	import argparse
import sys


 desc = 'Tool to check for error messages in a log file. By default ERROR, FATAL \	desc = 'Tool to check for error messages in a log file. By default ERROR, FATAL \
  and CRITICAL messages are considered. The config file may be used to \	  and CRITICAL messages are considered. The config file may be used to \
@@ -51,6 +52,7 @@ def parseOptions():
    print(args)	    print(args)
    if not (args.errors or args.warnings): #Will have to make it |not args.noterrors| if change made in line 42.	    if not (args.errors or args.warnings): #Will have to make it |not args.noterrors| if change made in line 42.
        print('error: at least one of errors and warnings must be enabled')	        print('error: at least one of errors and warnings must be enabled')
        sys.exit(4)


 def parseConfig():	def parseConfig():
    global ignorePattern	    global ignorePattern
@@ -79,18 +81,22 @@ def scanLogfile():
    #print(igLevels)	    #print(igLevels)
    #print(pattern)	    #print(pattern)
    logFileAddress = args.logfile	    logFileAddress = args.logfile
    with open(logFileAddress,'r') as logFile:	    try:
        tracing = False	        with open(logFileAddress,'r') as logFile:
        for line in logFile:	            tracing = False
            if re.search(tPattern,line):	            for line in logFile:
                tracing = True	                if re.search(tPattern,line):
            elif line =='\n':	                    tracing = True
                tracing = False	                elif line =='\n':
            if re.search(msgLevels,line):	                    tracing = False
                #print('Accepted',line);	                if re.search(msgLevels,line):
                resultsA.append(line)	                    #print('Accepted',line);
            elif tracing:	                    resultsA.append(line)
                resultsA.append(line)	                elif tracing:
                    resultsA.append(line)
    except:
        sys.exit(2)

     if args.showexcludestats:	    if args.showexcludestats:
        seperateIgnoreRegex = [re.compile(line) for line in ignorePattern]	        seperateIgnoreRegex = [re.compile(line) for line in ignorePattern]
        global ignoreDict	        global ignoreDict
@@ -118,6 +124,6 @@ def printResults():
    if len(results) > 0:	    if len(results) > 0:
        for msg in results: print(msg.strip('\n'))	        for msg in results: print(msg.strip('\n'))
        print("FAILURE : error/fatal found in log file - see",logFileAddress,"\nNB replace rel_0 with actual nightly in this URL.")	        print("FAILURE : error/fatal found in log file - see",logFileAddress,"\nNB replace rel_0 with actual nightly in this URL.")
			        sys.exit(10)


 main()	main() # added exit codes 256 - old_code = new_code
