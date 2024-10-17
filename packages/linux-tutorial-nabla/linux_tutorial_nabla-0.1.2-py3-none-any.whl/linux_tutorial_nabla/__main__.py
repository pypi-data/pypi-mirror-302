from linux_tutorial_nabla.terminal import Terminal
from linux_tutorial_nabla.tab_completer import TabCompleter
import readline
import sys
def main():
    if sys.platform != "linux":
        print("This program is only supported on Linux")
        exit()
    readline.set_completer_delims('\t')
    readline.parse_and_bind('tab: complete')
    tab_completer = TabCompleter()
    readline.set_completer(tab_completer.completer)
    terminal = Terminal()
    terminal.run()
