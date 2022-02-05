import messages as msg
import helpers, glob

# settings = helpers.get_settings()

def execute(ARGS):
	argDict = helpers.arguments(ARGS)
	filepath = helpers.kv_set(argDict, 'file')
	destination = helpers.kv_set(argDict, 'to')

	checkforSVGO = 'npm list -g | grep svgo'
	hasSVGO = helpers.run_command_output(checkforSVGO, False)
	installSVGO = 'npm install -g svgo'
	installSVGOWithSudo = 'sudo npm install -g svgo'

	if hasSVGO is None:
		msg.installing_svgo()
		useSudo = helpers.user_selection('Use Sudo? ', ['Yes', 'No'], )
		if useSudo is 1:
			helpers.run_command(installSVGOWithSudo)
		elif useSudo is 2:
			helpers.run_command(installSVGO)
	else:
		if filepath:
			helpers.run_command('svgo {FILE} -o {FILE}.optimized --pretty'.format(FILE = filepath))
		else:
			dir = helpers.path('current')
			msg.working_from(dir)
			fileList = [f for f in glob.glob("*.svg")]
			selectedFileList = helpers.user_selection('Selection: ', fileList, True)
			if selectedFileList is 'exit':
				msg.exiting()
			else:
				if not destination:
					destination = dir
				for index in selectedFileList:
					svgFile = fileList[index - 1]
					svgFileCore = svgFile.replace('.svg', '')
					helpers.run_command('svgo {DIR}/{FILE} -o {DESTINATION}/{FILE_CORE}-clean.svg --pretty'.format(DIR = dir.replace('\n', ''), DESTINATION = destination.replace('\n', ''), FILE = svgFile, FILE_CORE = svgFileCore))

	msg.done()
