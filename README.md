# SVG #

[ svg clean ]           removes cruft. Available Options:


file:           Specify a specific file by path

batch:          't/true', Processes all files in the current directory, or the 'from' path

from:           Path/directory to work from.
                Use the value '-profile-' to utilize your profile's 'fromPath'

to:             Path/directory to save files to.
                Use the value '-profile-' to utilize your profile's 'toPath'

profile:        't/true', Uses the 'fromPath' and 'toPath' values from your profile file


[ svg format ]          optimizes svgs using Inkscape

[ svg minifiy ]         Shares the same functionality as 'clean',
                        but removes whitespace characters, as well