import messages as msg
import helpers, glob, re

settings = helpers.get_settings()

def execute(ARGS):
	argDict = helpers.arguments(ARGS)
	filePath = helpers.kv_set(argDict, 'file')
	batch = helpers.kv_set(argDict, 'batch')
	origin = helpers.kv_set(argDict, 'from')
	destination = helpers.kv_set(argDict, 'to')
	profile = helpers.kv_set(argDict, 'profile')
	formatStrokes = helpers.kv_set(argDict, 'strokes')

	hasSVGO = helpers.handle_svgo()

	#= if SVGO is installed, proceed!
	if hasSVGO:
		batch = True if (batch == 't' or batch == 'true') else False
		profile = True if (profile == 't' or profile == 'true') else False
		formatStrokes = True if (formatStrokes == 't' or formatStrokes == 'true') else False

		if profile:
			fromPath = helpers.normalize_tilde(settings['fromPath'])
			toPath = helpers.normalize_tilde(settings['toPath'])
		else:
			fromPath = helpers.normalize_tilde(origin) if origin else helpers.path('current')
			toPath = helpers.normalize_tilde(destination) if destination else helpers.path('current')

			if fromPath == '-profile-':
				fromPath = helpers.normalize_tilde(settings['fromPath'])
			if toPath == '-profile-':
				toPath = helpers.normalize_tilde(settings['toPath'])

		#= If filePath is specified:
		if filePath:
			rootDir = fromPath or re.findall('[\~.\d\D]*/', filePath)[0][:-1]
			rootDest = toPath or rootDir
			svgFile = re.findall('[^\/]*\.svg', filePath)[0]

			helpers.format(rootDir, rootDest, svgFile, formatStrokes)

		#= if filePath is NOT specified, select from list or do as a batch
		else:
			paramStr = "{}/*.svg".format(fromPath)
			fileList = [f for f in glob.glob(paramStr)]
			orderedFileList = sorted(fileList, key=str.lower)
			nameOnlyFileList = helpers.strip_path(orderedFileList, fromPath)

			if batch:
				for svgFile in nameOnlyFileList:
					helpers.format(fromPath, toPath, svgFile, formatStrokes)
				
			else:
				msg.working_from(fromPath)
				selectedFileList = helpers.user_selection('Selection: ', nameOnlyFileList, True)

				if selectedFileList is 'exit':
					msg.exiting()
				else:
					for index in selectedFileList:
						svgFile = nameOnlyFileList[index - 1]
						helpers.format(fromPath, toPath, svgFile, formatStrokes)	

	msg.done()
