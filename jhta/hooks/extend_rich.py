import os
import rich
from cement.utils import fs


def extend_rich(app):
    app.log.debug('extending jhta application with rich console')
    app.extend('console', rich.console.Console())

