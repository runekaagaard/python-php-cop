import urwid, urwid.curses_display
import os
import re
import sys
import time

class PhpCop(object):
    def __init__(self):
        self.file = sys.argv[1]
        self.init_urwid()
    
    def init_urwid(self):
        self.ui = urwid.curses_display.Screen()
        self.ui.register_palette([
            ('default', 'default', 'default'),
            ('warn', 'light red', 'default'),
            ('stacktrace', 'light green', 'default'),
            ('bg', 'black', 'dark blue')
        ])

        self.frame = urwid.Frame(self.get_columns(), "", "", focus_part='body')
        self.box = urwid.AttrWrap(self.frame, 'default')
        self.ui.run_wrapper(self.main)

    def get_columns(self):
        errors = []
        for line in open(self.file).readlines():
            if line.strip() == "":
                continue
            line = line.strip()
            if "on line" in line:
                stacktrace = []
                errors.append((line, stacktrace))
            else:
                stacktrace.append(line)
        
        parts = []
        i = 0
        for (error, stacktraces) in errors:
            if "Notice:" in error:
                color = "default"
            else:
                color = "warn"
            parts.append(urwid.AttrWrap(urwid.Text(error, wrap='clip'), color))
            for s in stacktraces:
                parts.append(urwid.AttrWrap(urwid.Text(s, wrap='clip'), "stacktrace"))
            i += 1
        return urwid.Columns([urwid.ListBox(parts)], dividechars=1, focus_column=0)

    def main(self):
        while True:
            self.size = self.ui.get_cols_rows()
            self.canvas = self.box.render(self.size)
            self.frame.set_body(self.get_columns())
            self.ui.draw_screen(self.size, self.canvas)
            time.sleep(0.5)
PhpCop()

'''
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
'''