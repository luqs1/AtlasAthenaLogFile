import logtest

invigilator = logtest.Test()

testExpected = {"athena.log.1": 10, "athena.log.2": 10, "athena.log": 0}
testOutcome = testExpected.copy()


def testlog(logName, expectedValue):
    realValue = invigilator.testcase(logName,config='t.conf')
    return (realValue == expectedValue) # fix this


for k, v in testExpected.items():
	testOutcome[k] = testlog(k, v)
