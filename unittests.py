class Test:
	def errorcode(self,str0):
		if 'EXIT' in str0:
			return True
		else:
			return False

	def testcase(self,logFileAddress,kwargs**):
		if 'config' in kwargs:
			configFileAddress = kwargs['config']
		else:
			configFileAddress = 'check_log.conf'
		
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

		tuple1=self.parseConfig(configFileAddress)
		if self.errorcode(tuple1):return tuple1[-1]

		ignorePattern = tuple1
		tuple2 = self.scanLogFile(logFileAddress,ignorePattern,cWarnings,cErrors)
		if self.errorcode(tuple2):return tuple2[-1]

		msgLevels,results,ignoreDict,extra = tuple2
		exitcode = self.printResults(logFileAddress,msgLevels,ignoreDict,results,cErrors,cWarnings,cStats,extra)
		return exitcode

	def parseConfig(self,confAddress):

		ignorePattern = []
		try:
			with open(confAddress,'r') as configFile:
				for aline in configFile:
					if 'ignore' in aline:
						line = aline.strip('ignore').strip().strip("'")
						ignorePattern.append(line)
		except:
			print(confAddress+'has not been found.')
			return ('ERROR',1)

	def scanLogFile(self,logFileAddress,ignorePattern,cWarnings,cErrors):
		excludeStats = 0
		resultsA =[]
		pattern = []
		tPattern = re.compile('|'.join(traceback))
		if args.warnings == True:
			pattern.extend(warningRegex)
		if args.errors == True:
			pattern.extend(errorRegex)
		msgLevels = re.compile('|'.join(pattern))
		#print(msgLevels)
		igLevels = re.compile('|'.join(ignorePattern))
		#print(igLevels)
		#print(pattern)
		logFileAddress = args.logfile
		try:
			with open(logFileAddress,'r') as logFile:
				tracing = False
				for line in logFile:
					if re.search(tPattern,line):
						tracing = True
					elif line =='\n':
						tracing = False
					if re.search(msgLevels,line):
						#print('Accepted',line);
						resultsA.append(line)
					elif tracing:
						resultsA.append(line)
		except:
			sys.exit(2)
		if args.showexcludestats:
			seperateIgnoreRegex = [re.compile(line) for line in ignorePattern]
			global ignoreDict
			ignoreDict = {line:False for line in ignorePattern}       
		global results
		results = []
		for i in range(len(resultsA)):
			if not re.search(igLevels,resultsA[i]):
				results.append(resultsA[i])
			elif args.showexcludestats:
				for i in range(len(seperateIgnoreRegex)):
					if re.search(seperateIgnoreRegex[i],line):
						ignoreDict[ignorePattern[i]] = True
		#print('FINAL',results)

	def PrintResults(self,logFileAddress,msgLevels,ignoreDict,results,cErrors,cWarnings,cStats,extra):
		if cStats:
			print('Ignored:')
			for i in ignoreDict:
				if ignoreDict[i]:
					print(i)
			print('\n')
		print('Found messages in',logFileAddress,':')
		if len(results) > 0:
			for msg in results: print(msg.strip('\n'))
				print("FAILURE : error/fatal found in log file - see",logFileAddress,"\nNB replace rel_0 with actual nightly in this URL.")
			sys.exit(10)
