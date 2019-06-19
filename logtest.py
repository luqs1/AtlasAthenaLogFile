import os
class Test:
    def __init__(self):
        pass
    def testcase(self,fileAddress,config,**kwargs):
        exitCode = os.system('python check_log.py --config '+config+' '+fileAddress + ' >ignore.txt')
        os.system('rm ignore.txt')
        return exitCode

