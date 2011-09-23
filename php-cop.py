import urwid, urwid.curses_display
import os
import re
import sys
import time
import argparse
from pprint import pprint

class PhpCop(object):
    def __init__(self, args):
        self.args = args
        self.init_urwid()
    
    def init_urwid(self):
        self.ui = urwid.curses_display.Screen()
        self.ui.register_palette([
            ('default', 'default', 'default'),
            ('warn', 'light red', 'default'),
            ('date', 'dark gray', 'default'),
            ('level', 'dark green', 'default'),
            ('content', 'default', 'default'),
            ('file', 'brown', 'default'),
            ('lineno', 'light cyan', 'default'),
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
    
    patterns = (
        ('stack_title', re.compile(r'^\[(?P<date>.*)] PHP Stack trace:$')),
        ('stack_content', re.compile(
            r'^\[(?P<date>.*)] PHP   [0-9]+. ' 
            r'(?P<content>.*) (?P<file>/.*):(?P<lineno>[0-9]+)$')),
        ('func_error', re.compile(
            r'^\[(?P<date>.*)] ([^:]+):  (?P<content_a>.*) called in '
            r'(?P<file_a>/.*) on line (?P<lineno_a>[0-9]+) and defined in '
            r'(?P<file_b>/.*) on line (?P<lineno_b>[0-9]+)')),
        ('error', re.compile(
            r'^\[(?P<date>.*)] PHP (?P<level>.*):  (?P<content>.*) in '
            r'(?P<file>/.*) on line (?P<lineno>[0-9]+)$')),
        ('other', re.compile(r'(.*)')),
    )
    
    def parse_file(self):
        file_structure = []
        for line in self.args.logfile.readlines():
            for name,pattern in self.patterns:
                match = pattern.match(line)
                if match:
                    if name not in ('stack_title', 'stack_content'):
                        file_structure.append((name, match, []))
                    else:
                        # Support badly formatted files, that starts with a
                        # stacktrace.
                        try:
                            file_structure[-1][2].append([name, match])    
                        except IndexError:
                            file_structure.append((name, match, []))
                    break
        self.args.logfile.seek(0)
        return file_structure
    
    def render_columns(self):
        def stack_title(match): return None
        def stack_content(match): return None
        def func_error(match): return None
        
        def format_date(date):
            return date[-8:]
            
        def error(gd):
            ##color = get_color(error)
            #print gd; sys.exit()
            return urwid.Text([
                ('date', format_date(gd['date'])),
                ('default', ' '),
                ('level', gd['level']),
                ('default', ': '),
                ('content', gd['content']),
                ('content', '. '),
                ('file', gd['file']),
                ('default', ':'),
                ('lineno', gd['lineno']),
            ])
            return urwid.AttrWrap(urwid.Text("YO", wrap='clip'), 'default')
        
        def other(match): return None 
        
        def render_stacktrace(stacktrace):
            return urwid.AttrWrap(urwid.Text(stacktrace, wrap='clip'), 
                                  "stacktrace")
        
        funcs = {'stack_title': stack_title, 'stack_content': stack_content,
                 'func_error': func_error, 'error': error, 'other': other}
        columns = []
        for (line_type, match, stacktraces) in self.parse_file():
            column = funcs[line_type](match.groupdict())
            if column:
                columns.append(column)
            for stacktrace in stacktraces:
                pass
        
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
