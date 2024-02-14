from rich.panel import Panel


def render(context):
    return Panel('[bold green]:green_circle: %s [/]' % context['msg'])

