import sys, sizzle
import messages as msg
import Clean
import Format
import Minify
# new imports start here

# settings = helpers.get_settings()

try:
	action = str(sys.argv[1])
except:
	action = None

args = sys.argv[2:]

if action == None:
	msg.statusMessage()

elif action == '-action':
	sizzle.do_action(args)

elif action == '-profile':
	sizzle.profile()

elif action == '-helpers':
	sizzle.helpers()

elif action == '-alias':
	sizzle.alias()

elif action == "clean":
	Clean.execute(args)

elif action == "minify":
	Minify.execute(args)

elif action == "format":
	Format.execute(args)
# new actions start here
