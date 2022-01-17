#!/usr/bin/env python3

"""
combine both a python shell and an linux shell
"""

import numpy as np
import math
import os
import re
import readline
import subprocess
import shlex
import sys

from io import StringIO
from contextlib import redirect_stdout


COMMANDS = ['cd']
RE_SPACE = re.compile('.*\s+$', re.M)
SHELL_PATH = '/bin/zsh'

# https://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
class Completer(object):

    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def _complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete_cd(self, args):
        "Completions for the 'cd' command."
        if not args:
            return self._complete_path('.')
        # treat the last arg as a path and complete it
        return self._complete_path(args[-1])

    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in COMMANDS][state]
        # account for last argument ending in a space
        if RE_SPACE.match(buffer):
            line.append('')
        # resolve command to the implementation function
        cmd = line[0].strip()
        args = line[1:]
        if cmd in COMMANDS:
            impl = getattr(self, 'complete_%s' % cmd)
            if args:
                return (impl(args) + [None])[state]

            return [cmd + ' '][state]
        else:
            if args:
                return (self.complete_cd(args) + [None])[state]

            results = [c + ' ' for c in COMMANDS if c.startswith(cmd)] + [None]
            return results[state]


def execute_shell_to_stdout(command):
    subprocess.run(
            command, 
            shell=True,
            executable=SHELL_PATH
    )



def main():
    # enable tab completion
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(Completer().complete)

    # loop through stdin
    while True:
        try:
            # get input
            command = input(f'{os.getcwd().replace(os.path.expanduser("~"), "~", 1)} > ').strip()

            # if command starts with %, it is an inline pyhton operation
            # so command = 'temp = ' + command
            # afterwards print temp
            if command.startswith('$'):
                command = 'temp=' + command.lstrip('$') + ';print(temp);del temp'

            # split the input command in args and the base command
            command_split = shlex.split(command)

            command_0, command_args = '', []
            if len(command_split) >= 1:
                command_0 = command_split[0]
            if len(command_split) > 1:
                command_args = command_split[1:]

            

            # define actions of default commands
            if command_0 == 'exit':
                exit() 
            elif command_0 == 'cd':

                if not len(command_args):
                    os.chdir('~')
                else:
                    os.chdir(command_args[0])
            elif command_0 == 'clear' or command_0 == 'cls':
                os.system('clear')
            elif len(command_0) > 0:
                # if this scope has the given variable, print it
                if command in vars():
                    print(vars()[command])
                else:
                    # try executing python code with stdout,
                    # if it is not valid syntax, execute shell command
                    try:
                        stdout_redir = StringIO()
                        with redirect_stdout(stdout_redir):
                            exec(command)
                        print(stdout_redir.getvalue().strip())
                    except (NameError, SyntaxError):
                        execute_shell_to_stdout(command)

        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            exit()
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    main()

