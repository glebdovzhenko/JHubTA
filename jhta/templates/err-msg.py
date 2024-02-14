from rich.panel import Panel


def render(context):
    return Panel('[bold red]:x: :x: %s :x: :x:[/]' % context['msg'])

