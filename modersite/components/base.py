"""Define a HTML component class, a elaborated piece of template."""


class Component:
    """Base component class."""

    template: str = "components/base.html"

    def render(self, context):
        """Render the component."""
        return context.template.engine.get_template(self.template).render(context)
