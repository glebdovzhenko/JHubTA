
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from rich.panel import Panel


VERSION_BANNER = """
Assists in commont tasks while teaching a class using JupyterHub %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Assists in commont tasks while teaching a class using JupyterHub'

        # text displayed at the bottom of --help output
        epilog = 'Usage: jhta command1 --foo bar'

        # controller level arguments. ex: 'jhta --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

