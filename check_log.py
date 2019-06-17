import re
import argparse

desc = 'Tool to check for error messages in a log file. By default ERROR, FATAL \
  and CRITICAL messages are considered. The config file may be used to \
provide patterns of lines to exclude from this check - known false positives.'

epilogue = 'Note that at least one of errors and warnings must be true, otherwise there is nothing to search for.\
    Using --errors will disable errors.'

errorRegex = ["^ERROR | ERROR | FATAL |CRITICAL |ABORT_CHAIN",
"^Exception\:|^Caught signal|^Core dump|Traceback|Shortened traceback|stack trace|^Algorithm stack\:|IncludeError|ImportError|AttributeError|inconsistent use of tabs and spaces in indentation\
|glibc detected|tcmalloc\: allocation failed|athenaHLT.py\: error"]

warningRegex = ['WARNING']

def main():
    parseOptions()
    parseConfig()
    scanLogfile()
    #printResults()

def parseOptions():
    parser = argparse.ArgumentParser(description=desc, epilog=epilogue)
    parser.add_argument('logfile',metavar='<logfile>')
    parser.add_argument('--config',
    metavar='<file>',
    type = str,
    help ='specify config file (default is check_log.conf) will be got from DATAPATH if it does not exist',
    default='check_log.conf'
    )
    parser.add_argument('--showexcludestats',
    action = 'store_true',
    default = False,
    help ='print a summary table of the number of times each of the exclude patterns was matched (default False)'
    )
    parser.add_argument('--warnings',
    action = 'store_true',
    default = False,
    help ='check in addition for WARNING messages (default False)'
    )
    parser.add_argument('--errors', #thinking of changing to --noerrors? will check based on usage in existing system. Highly recommend.
    action = 'store_false',
    default = True,
    help = 'check errors (default true)'
    )
    global args
    args = parser.parse_args()
    print(args)
    if not (args.errors or args.warnings): #Will have to make it |not args.noterrors| if change made in line 42.
        print('error: at least one of errors and warnings must be enabled')

def parseConfig():
    global ignorePattern
    ignorePattern = []
    configFileAddress = args.config
    with open(configFileAddress,'r') as configFile:
        for aline in configFile:
            if 'ignore' in aline:
                line = aline.strip('ignore').strip().strip("'")
                ignorePattern.append(line)
    print(ignorePattern)
def scanLogfile():
    excludeStats = 0
    results =[]
    pattern = []
    if args.warnings == True:
        pattern.extend(warningRegex)
    if args.errors == True:
        pattern.extend(errorRegex)
    msgLevels = re.compile('|'.join(pattern))
    print(msgLevels)
    igLevels = re.compile('|'.join(ignorePattern))
    print(igLevels)
    #print(pattern)
    logFileAddress = args.logfile
    with open(logFileAddress,'r') as logFile:
        for line in logFile:
            if re.search(msgLevels,line):
                print('Accepted',line);
                results.append(line)
    results1 = []
    for i in range(len(results)):
        if not re.search(igLevels,results[i]):
            pass
        else:
            results1.append(results[i])
main()
