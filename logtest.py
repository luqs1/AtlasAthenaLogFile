
# Returns check_log's exit code for a given log
# Used to test check_log is working correctly
import subprocess
class Test:
    def __init__(self):
        pass
    def testcase(self,fileAddress,**kwargs):
        modifiers= ''
        if 'config' in kwargs:
            config = kwargs['config']
        else:
            config = 'test_log.conf'
        if 'errors' in kwargs:	
            cErrors = kwargs['errors']	
        else:	
            cErrors = True
        if 'warnings' in kwargs:	
            cWarnings = kwargs['warnings']	
        else:	
            cWarnings = False	
        if 'showExcludeStats' in kwargs:	
            cStats = kwargs['showExcludeStats']	
        else:
            cStats = False
        if not (cErrors or cWarnings):	
            return 4
        if not cErrors: #if --noerrors change has been made, remove not
            modifiers += '--errors' #and make this --noerrors
        if cWarnings:
            modifiers += '--warnings'
        if cStats:
            modifiers += '--showexcludestats'
        exitCode = subprocess.call('python check_log.py --config '+config+' '+modifiers+' ' +fileAddress +' >tempoutlog.txt', shell = True) #if upgrading to Python 3+, this
        subprocess.call('rm tempoutlog.txt', shell = True) #and this require changing
        return exitCode
