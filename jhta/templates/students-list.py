from rich.table import Table
from rich.console import Group

def render(context):
    result = []
    for g_id in sorted(context['group_ids'].keys()):
        tb = Table(title='%s (%s)' % (context['group_ids'][g_id], g_id))
        tb.add_column("Login", justify="right", style="cyan", no_wrap=True)
        tb.add_column("Name", style="magenta")
        for st in sorted(context['students'], key=lambda x: x['surname']):
            if st['group_id'] == g_id:
                tb.add_row(st['login'], '[bold]%s[/] %s' % (st['surname'], st['name']))
        result.append(tb)
    return Group(*result)
