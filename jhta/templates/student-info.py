from rich.table import Table
from rich.console import Group
from rich.text import Text
from rich.padding import Padding
from rich.panel import Panel

def render(context):
    return Panel(Group(
        '     ФИО: [bold magenta]%s[/] [magenta]%s[/]' % (context['surname'], context['name']),
        '  Группа: [cyan]%s(%s)[/]' % (context['group'], context['group_id']),
        '   Логин: [cyan]%s[/]' % context['login']
        ))
