import helpers, json

actionList = json.loads(helpers.read_file('{}/{}'.format(helpers.path('util'), 'action-list.json')))

def statusMessage():
	if len(actionList['actions']) > 0:
		print("")
		for item in actionList['actions']:
			print('''[ {} {} ]\t\t{}'''.format(actionList['alias'], item['name'], item['description']))
		print("")
	else:
		print('''
SVG is working successfully!
''')

def done():
	print('''
[ Process Completed ]
''')

def installing_svgo():
	print('''
SVGO not found. Installing now ...
''')

def add_filepath():
	print('''

filepath required. Example: svg clean file:some/file/path.svg
''')

def working_from(DIR):
	print('''
Currently working from: {}
'''.format(helpers.decorate('green', DIR)))

def exiting():
	print('''

Exiting ...''')