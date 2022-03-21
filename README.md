# SVG #

\~\~\~ Made with [Bacon](https://github.com/jaderigby/bacon)!

## Setup ##

The SVG Utility is a Bacon utility.  If you haven't already, follow the instructions for installing [Bacon](https://github.com/jaderigby/bacon#setup).  Once Bacon is installed: Either 1) clone or 2) download, unzip and move the SVG Utility to the bacon-bits folder contained within your Documents folder.

Then, run `bacon alias` and `bacon set`.  That's it!  To check that everything is running, type `svg` then hit enter and you should see the usage instructions for the SVG Utility.

### Clean ###

`svg clean`

Clean removes cruft. See the "Available Options" below for more details.  Using just `svg clean` will give you a selection list to choose from.  Once a file is selected, it will be saved in the same location as the original, and the extension `.clean.svg` will be added.  For example, `some-file.svg` will be saved as `some-file.clean.svg`.  The original will remain untouched.

To save the cleaned file to a specific location, use the `to` attribute.

For example: `svg clean to:~/Downloads`.  This will save the new "clean" file to your Downloads folder.

If you want to set a folder to use every time, first create a profile file by running `svg -profile`.  This will generate a profile file within your svg repo.  Then, open the file and add the following:

```
{
	"settings" : {
		"toPath" : "~/Documents/test-clean"
	}
}
```

Save it, and when you want to use this path, simply use the value `-profile-` for the `to` attribute, like so:  `svg clean to:-profile-`.


Available Options (for clean, format, and minify):

- __file:__           Specify a specific file by path

- __batch:__          't|true', Processes all files in the current directory, or the 'from' path

- __from:__           Path/directory to work from.
Use the value '-profile-' to utilize your profile's 'fromPath'

- __to:__             Path/directory to save files to.
                Use the value '-profile-' to utilize your profile's 'toPath'

- __profile:__        't|true', Uses the 'fromPath' and 'toPath' values from your profile file

### Format ###

`svg format`

Format optimizes svgs using Inkscape.  If you'd like to formath strokes to paths, as well, add the argument 'strokes:t' or 'strokes:true'. For example:

```
svg format strokes:t

```

### Minify ###

`svg minify`

Minify shares the same functionality as 'clean', but removes whitespace characters, as well.