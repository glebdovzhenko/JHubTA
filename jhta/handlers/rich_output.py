from cement.core.output import OutputHandler
from cement.core.template import TemplateHandler
from cement.utils.misc import minimal_logger
from importlib import import_module

LOG = minimal_logger(__name__)


class RichOutputHandler(OutputHandler):
    class Meta:
        label = 'rich'

    def __init__(self, *args, **kw):
        super(RichOutputHandler, self).__init__(*args, **kw)
        self.templater = None

    def _setup(self, app):
        super(RichOutputHandler, self)._setup(app)
        self.templater = self.app.handler.resolve('template', 'rich',
                                                  setup=True)

    def render(self, data, template=None, **kw):
        """
        Render the given ``content`` as template with the ``data`` dictionary.

        Args:
            content (str): The template content to render.
            data (dict): The data dictionary to render.

        Returns:
            str: The rendered template text

        """
        LOG.debug("rendering content using '%s' as a template." % template)
        content, _type, _path = self.templater.load(template)
        return self.templater.render(_path, data)


class RichTemplateHandler(TemplateHandler):

    """
    This class implements the :ref:`Template <cement.core.template>` Handler
    interface.  It renders content as template, and supports copying entire
    source template directories using the
    `Jinja2 Templating Language <http://jinja.pocoo.org/>`_.  Please
    see the developer documentation on
    :cement:`Template Handling <dev/template>`.
    """

    class Meta:

        """Handler meta-data."""

        label = 'rich'

    def load(self, *args, **kw):
        """
        Loads a template file first from ``self.app._meta.template_dirs`` and
        secondly from ``self.app._meta.template_module``.  The
        ``template_dirs`` have presedence.

        Args:
            template_path (str): The secondary path of the template **after**
                either ``template_module`` or ``template_dirs`` prefix (set via
                ``App.Meta``)

        Returns:
            tuple: The content of the template (``str``), the type of template
            (``str``: ``directory``, or ``module``), and the path (``str``) of
            the directory or module)

        Raises:
            cement.core.exc.FrameworkError: If the template does not exist in
                either the ``template_module`` or ``template_dirs``.
        """
        content, _type, _path = super(RichTemplateHandler, self).load(*args,
                                                                        **kw)

        return content, _type, _path

    def render(self, _path, data, *args, **kw):
        """
        Render the given ``content`` as template with the ``data`` dictionary.

        Args:
            content (str): The template content to render.
            data (dict): The data dictionary to render.

        Returns:
            str: The rendered template text

        """
        LOG.debug("rendering content as text via %s" % self.__module__)
        
        return import_module(_path.replace('.py', '')).render(data)
        
