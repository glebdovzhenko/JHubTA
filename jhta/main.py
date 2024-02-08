
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import JHTAppError
from .controllers.base import Base
from .controllers.students import Students
from .handlers.rich_output import RichOutputHandler, RichTemplateHandler
from .hooks.extend_tinydb import extend_tinydb
from .hooks.extend_rich import extend_rich

# configuration defaults
CONFIG = init_defaults('jhta')
CONFIG['jhta']['db_file'] = '~/.jhta/db.json'


class JHTApp(App):
    """JupyterHub Teaching Assistant primary application."""

    class Meta:
        label = 'jhta'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            # 'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        # output_handler = 'jinja2'

        output_handler = 'rich'
        template_handler = 'rich'

        # register handlers
        handlers = [
            Base,
            Students,
            RichOutputHandler,
            RichTemplateHandler
        ]

        # register hooks
        hooks = [
            ('post_setup', extend_tinydb),
            ('post_setup', extend_rich),
        ]


class JHTAppTest(TestApp,JHTApp):
    """A sub-class of JHTApp that is better suited for testing."""

    class Meta:
        label = 'jhta'


def main():
    with JHTApp() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except JHTAppError as e:
            print('JHTAppError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
