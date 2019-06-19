import unittest

testExpected = {"athena.log.1": 10, "athena.log.2": 10, "athena.log": 0}
testOutcome = testExpected.copy()


def testlog(logName, expectedValue):
	return(assertEqual(RESULTOFTEST, expectedValue)) # fix this

#test = Test() 
#test.testlog()

for k, v in testLogs.items():
	testOutcome[k] = testlog(k, v)
