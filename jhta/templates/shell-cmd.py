from rich.table import Table
from rich.console import Group
from rich.text import Text
from rich.padding import Padding
from rich.panel import Panel

def render(context):
    out = ['[bold magenta]     CMD:[/][cyan] %s [/]' % context['cmd'],
            '[bold magenta] retcode:[/][cyan] %d[/]' % context['retcode']]
    if context['err']:
        out.append('[bold magenta]  STDERR:[/][cyan]\n%s[/]' % context['err'].decode())
    if context['out']:
        out.append('[bold magenta]  STDOUT:[/][cyan]\n%s[/]' % context['out'].decode())

    return Panel(Group(*out))

