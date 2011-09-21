import urwid
import os
import re
from pprint import pprint
import sys

"""
'default' (use the terminal's default foreground),
'black', 'dark red', 'dark green', 'brown', 'dark blue',
'dark magenta', 'dark cyan', 'light gray', 'dark gray',
'light red', 'light green', 'yellow', 'light blue', 
'light magenta', 'light cyan', 'white'
 """
palette = [
    ('default', 'default', 'default'),
    ('warn', 'light red', 'default'),
    ('stacktrace', 'light green', 'default'),
    ('bg', 'black', 'dark blue'),]

txt = urwid.Text(('default', ""))
map1 = urwid.AttrMap(txt, 'default')
fill = urwid.Filler(map1, valign='top')
current_open_stacktrace = -1
ignores = []

def update_screen():
	errors = []
	for line in open(sys.argv[1]).readlines():
		if "on line" in line:
			stacktrace = []
			errors.append((line, stacktrace))
		else:
			stacktrace.append(line)
	
	parts = []
	i = 0
	for (error, stacktraces) in errors:
		if i in ignores:
			i += 1
			continue
		if "Notice:" in error:
			color = "default"
		else:
			color = "warn"
		parts.append((color, error))
		for s in stacktraces:
			if i == current_open_stacktrace:
				parts.append(("default", "    "))
				parts.append(("stacktrace", s))
		i += 1
	txt.set_text(parts)

def exit_on_q(input):
	global current_open_stacktrace, ignores
	if input in ('s',):
		current_open_stacktrace += 1
	if input in ('a',):
		current_open_stacktrace -= 1
	if input in ('i',):
		ignores.append(current_open_stacktrace)
	if input in ('q', 'Q'):
		raise urwid.ExitMainLoop()
	update_screen()

	
update_screen()
loop = urwid.MainLoop(fill, palette, unhandled_input=exit_on_q)
loop.run()