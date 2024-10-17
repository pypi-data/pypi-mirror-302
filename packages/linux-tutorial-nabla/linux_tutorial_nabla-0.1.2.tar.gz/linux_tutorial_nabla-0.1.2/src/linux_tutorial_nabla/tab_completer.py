import glob
import os
from linux_tutorial_nabla.common import TUTORIALS, NablaModel

commands = [
    "home","cd","ls","pwd","mkdir","touch","rm","rmdir","mv","cp","cat","echo","clear","exit","help", "nablahelp", "file",
    "status", "start", "reset"
]

commands.extend(TUTORIALS.ALL)

class TabCompleter(NablaModel):
    commands: list[str] = commands

    def get_path_options(self, text: str):
        last_part = text.split()[-1]

        if '~' in last_part:
            last_part = os.path.expanduser(last_part)

        if os.path.isdir(last_part):
            last_part += '/'

        paths = [text + x.removeprefix(last_part) for x in glob.glob(text + '*')]

        return paths
    
    def get_command_options(self, text: str):
        last_part = text.split()[-1]

        commands = [text + x.removeprefix(last_part) for x in self.commands if x.startswith(last_part)]

        return commands

    def completer(self, text, state):
        options = self.get_command_options(text)
        options.extend(self.get_path_options(text))

        if state < len(options):
            return options[state]
        else:
            return None