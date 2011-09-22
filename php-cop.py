import urwid, urwid.curses_display
import os
import re
import sys
import time
import argparse

class PhpCop(object):
    def __init__(self, args):
        self.args = args
        self.init_urwid()
    
    def init_urwid(self):
        self.ui = urwid.curses_display.Screen()
        self.ui.register_palette([
            ('default', 'default', 'default'),
            ('warn', 'light red', 'default'),
            ('stacktrace', 'light green', 'default'),
            ('bg', 'black', 'dark blue')
        ])

        self.frame = urwid.Frame(self.render_columns(), "", "", focus_part='body')
        self.box = urwid.AttrWrap(self.frame, 'default')
        self.ui.run_wrapper(self.main)
        
    def main(self):
        while True:
            self.size = self.ui.get_cols_rows()
            self.canvas = self.box.render(self.size)
            self.frame.set_body(self.render_columns())
            self.ui.draw_screen(self.size, self.canvas)
            time.sleep(0.5)
    
    def parse_file(self):
        file_structure = []
        for line in self.args.logfile.readlines():
            if line.strip() == "":
                continue
            line = line.strip()
            
            if "on line" in line:
                stacktrace = []
                file_structure.append((line, stacktrace))
            else:
                stacktrace.append(line)
        
        self.args.logfile.seek(0)
        return file_structure
    
    def render_columns(self):
        def get_color(error):
            if "Notice:" in error:
                return "default"
            else:
                return "warn"
        
        def render_error(error):
            color = get_color(error)
            return urwid.AttrWrap(urwid.Text(error, wrap='clip'), color)
            
        def render_stacktrace(stacktrace):
            return urwid.AttrWrap(urwid.Text(stacktrace, wrap='clip'), 
                                  "stacktrace")
                
        columns = []
        for (error, stacktraces) in self.parse_file():
            columns.append(render_error(error))
            for stacktrace in stacktraces:
                columns.append(render_stacktrace(stacktrace))
        
        return urwid.Columns([urwid.ListBox(columns)], dividechars=1, 
                             focus_column=0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Watch them PHP errors.')
    parser.add_argument('logfile', type=file, help="The logfile to watch")
    args = parser.parse_args()
    PhpCop(args)
    
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
