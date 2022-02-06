# SVG #

### Clean ###

`svg clean`

Clean removes cruft. Available Options:

- __file:__           Specify a specific file by path

- __batch:__          't/true', Processes all files in the current directory, or the 'from' path

- __from:__           Path/directory to work from.
Use the value '-profile-' to utilize your profile's 'fromPath'

- __to:__             Path/directory to save files to.
                Use the value '-profile-' to utilize your profile's 'toPath'

- __profile:__        't/true', Uses the 'fromPath' and 'toPath' values from your profile file

### Format ###

`svg format`

Format optimizes svgs using Inkscape.

### Minify ###

`svg format`

Minify shares the same functionality as 'clean', but removes whitespace characters, as well.