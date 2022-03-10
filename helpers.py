import json
from settings import settings
import messages as msg

profilePath = settings['profile_url'] + settings['profile']

def load_profile():
	import os
	return json.loads(read_file(profilePath)) if os.path.exists(profilePath) else json.loads("{}")

def get_settings():
	profile = load_profile()
	return profile['settings'] if 'settings' in profile else False

def path(TYPE):
	import os
	if TYPE == 'user':
		return os.path.expanduser('~/')
	elif TYPE == 'util' or TYPE == 'utility':
		return os.path.dirname(os.path.realpath(__file__))
	elif TYPE == 'curr' or TYPE == 'current':
		return run_command_output('pwd', False).replace('\n', '')
	else:
		return False

def read_file(FILEPATH):
	FILE = open(FILEPATH, 'r')
	data = FILE.read()
	FILE.close()
	return data

def write_file(FILEPATH, DATA):
	with open(FILEPATH, 'w') as f: f.write(DATA)

def run_command(CMD, option = True):
	import subprocess
	shellStatus = True
	str = ''
	showCmd = CMD
	if isinstance(CMD, list):
		shellStatus = False
		for item in CMD:
			str += (' ' + item)
		showCmd = str
	if option:
		print('\n============== Running Command: {}\n'.format(showCmd))
	subprocess.call(CMD, shell=shellStatus)

def run_command_output(CMD, option = True):
	import subprocess
	if option:
		print('\n============== Outputting Command: {}\n'.format(CMD))
	result = False
	if CMD != None:
		process = subprocess.Popen(CMD, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		out, err = process.communicate()

		if err:
			print(err)
		else:
			result = out.decode('utf-8')

	return result

def decorate(COLOR, STRING):
	bcolors = {
		 'lilac' : '\033[95m'
		,'blue' : '\033[94m'
		,'cyan' : '\033[96m'
		,'green' : '\033[92m'
		,'yellow' : '\033[93m'
		,'red' : '\033[91m'
		,'bold' : '\033[1m'
		,'underline' : '\033[4m'
		,'endc' : '\033[0m'
	}

	return bcolors[COLOR] + STRING + bcolors['endc']

def user_input(STRING):
	try:
		return raw_input(STRING)
	except:
		return input(STRING)

def list_expander(LIST):
    baseList = LIST.replace(' ', '').split(',')
    expandedList = []
    for item in baseList:
        if '-' in item:
            rangeList = item.split('-')
            tempList = [elem for elem in range(int(rangeList[0]), int(rangeList[1]) + 1)]
            expandedList += tempList
        else:
            expandedList.append(int(item))
    return expandedList

# generates a user selection session, where the passed in list is presented as numbered selections; selecting "x" or just hitting enter results in the string "exit" being returned. Any invaild selection is captured and presented with the message "Please select a valid entry"
def user_selection(DESCRIPTION, LIST, LIST_SELECT = False):
	import re
	str = ''
	for i, item in enumerate(LIST, start=1):
		str += '\n[{index}] {item}'.format(index=i, item=item)
	str += '\n\n[x] Exit\n'

	finalAnswer = False

	while True:
		print(str)
		selection = user_input('{}'.format(DESCRIPTION))
		pat = re.compile("[0-9,\- ]+") if LIST_SELECT else re.compile("[0-9]+")
		if pat.match(selection):
			selection = list_expander(selection) if LIST_SELECT else int(selection)
		if isinstance(selection, int) or isinstance(selection, list):
			finalAnswer = selection
			break
		elif selection == 'x':
			finalAnswer = 'exit'
			break
		elif selection == '':
			finalAnswer = 'exit'
			break
		else:
			print("\nPlease select a valid entry...")
	return finalAnswer

def arguments(ARGS, DIVIDER=':'):
	return dict(item.split('{}'.format(DIVIDER)) for item in ARGS)

def kv_set(DICT, KEY, DEFAULT = False):
	if KEY in DICT:
		DICT[KEY] = 't' if DICT[KEY] == 'true' else 'f' if DICT[KEY] == 'false' else DICT[KEY]
		return DICT[KEY]
	else:
		return DEFAULT


# custom helpers start here
# =========================

def handle_svgo():
	status = False
	checkforSVGO = 'npm list -g | grep svgo'
	hasSVGO = run_command_output(checkforSVGO, False)
	installSVGO = 'npm install -g svgo'
	installSVGOWithSudo = 'sudo npm install -g svgo'
	
	if hasSVGO is None:
		msg.installing_svgo()
		useSudo = user_selection('Use Sudo? ', ['Yes', 'No'], )
		if useSudo == 1:
			run_command(installSVGOWithSudo)
		elif useSudo == 2:
			run_command(installSVGO)
	else:
		status = True

	return status

#======================
# SHARED SUFFIX PATTERN
#======================
sharedSuffixPat = '(.designer.svg|.ink.svg|.sketch.svg|.formatted.svg|.clean.svg|.minified.svg|.svg|.serif-clean.svg)'

def clean(FROM, TO, FILE, TYPE):
	import re
	#= remove previous extensions, where possible:
	svgFileCore = re.sub(sharedSuffixPat, '', FILE)

	if TYPE == 'pretty':
		run_command("svgo '{FROM}/{FILE}' -o '{TO}/{FILE_CORE}.clean.svg' --pretty".format(FROM = FROM.replace('\n', ''), TO = TO.replace('\n', ''), FILE = FILE, FILE_CORE = svgFileCore))
	else:
		run_command("svgo '{FROM}/{FILE}' -o '{TO}/{FILE_CORE}.minified.svg'".format(FROM = FROM.replace('\n', ''), TO = TO.replace('\n', ''), FILE = FILE, FILE_CORE = svgFileCore))

def normalize_tilde(FILEPATH):
	import re
	firstChar = FILEPATH[:1]
	if firstChar == '~':
		return '{}{}'.format(path('user')[:-1], FILEPATH[1:])
	else:
		return FILEPATH

def strip_path(LIST, PATH):
	newList = []
	for item in LIST:
		newList.append(item.replace(PATH + '/', ''))
	return newList

def format(FROM, TO, FILE, STROKES_TO_PATH = True):
	import re

	#= remove previous extensions, where possible:
	svgFileCore = re.sub(sharedSuffixPat, '', FILE)
	
	run_command('scp {FROM}/{FILE} {TO}/{FILE_CORE}.formatted.svg'.format(FROM = FROM.replace('\n', ''), TO = TO.replace('\n', ''), FILE = FILE, FILE_CORE = svgFileCore))

	ct = 20

	while True:
		CONTENT = read_file('{TO}/{FILE_CORE}.formatted.svg'.format(TO = TO.replace('\n', ''), FILE_CORE = svgFileCore))
		match = False
		if ct > 0:
			ct -= 1
			match = re.findall('(<g |<g\n)', CONTENT)
			if match:
				run_command('inkscape --actions "select-all:groups; SelectionUnGroup; export-filename:{TO}/{FILE_CORE}.formatted.svg; export-plain-svg; export-do;" {TO}/{FILE_CORE}.formatted.svg'.format(TO = TO.replace('\n', ''), FILE_CORE = svgFileCore))
			else:
				print("completed!")
				break
		else:
			print("\n\n---- Maximum attempts achieved! ----\n")
			break

	run_command('inkscape --actions "select-all:no-groups;{FORMAT_STROKES} select-all:all; SelectionGroup; export-filename:{TO}/{FILE_CORE}.formatted.svg; export-plain-svg; export-do;" {TO}/{FILE_CORE}.formatted.svg'.format(TO = TO.replace('\n', ''), FILE_CORE = svgFileCore, FORMAT_STROKES = ' object-stroke-to-path;' if STROKES_TO_PATH else ''))

def serif_cleanup(FROM, TO, FILE):
	import re

	#= remove previous extensions, where possible:
	svgFileCore = re.sub(sharedSuffixPat, '', FILE)

	CONTENT = read_file('{FROM}/{FILE_CORE}.svg'.format(FROM = FROM.replace('\n', ''), FILE_CORE = svgFileCore))
	CONTENT_REFINED = re.sub('serif:id="[a-z A-Z0-9]*"', '', CONTENT)
	print('\nwriting file: {TO}/{FILE_CORE}.serif-clean.svg'.format(TO = TO.replace('\n', ''), FILE_CORE = svgFileCore))
	write_file('{TO}/{FILE_CORE}.serif-clean.svg'.format(TO = TO.replace('\n', ''), FILE_CORE = svgFileCore), CONTENT_REFINED)