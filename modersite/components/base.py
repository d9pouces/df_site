"""Define a HTML component class, a elaborated piece of template."""


class Component:
    """Base component class."""

    template: str = "components/base.html"

    def render(self, context):
        """Render the component in a HTML template."""
        self.update_render_context(context)
        return context.template.engine.get_template(self.template).render(context)

    def update_render_context(self, context):
        """Update the context before rendering the component."""
        pass
