"""Define a HTML component class, a elaborated piece of template.

A component should be instantiated once and not have any request-specific attribute.
Request-specific data should be passed as arguments to methods.
"""


class Component:
    """Base component class."""

    template: str = "components/base.html"

    def render(self, context, **kwargs):
        """Render the component in a HTML template.

        Context the complete template context.
        Kwargs is a dictionary of data provided to the template tag.
        """
        self.update_render_context(context, **kwargs)
        return context.template.engine.get_template(self.template).render(context)

    def update_render_context(self, context, **kwargs):
        """Update the context before rendering the component.

        Context the complete template context.
        Kwargs is a dictionary of data provided to the template tag.
        """
        pass
