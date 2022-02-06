import messages as msg
import helpers, glob
import Clean as clean

settings = helpers.get_settings()

def execute(ARGS):
	clean.execute(ARGS, 'minify')