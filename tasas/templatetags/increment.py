from django import template

register = template.Library()


class IncrementVariable(template.Node):
    def __init__(self, variable):
        self.variable = template.Variable(variable)

    def render(self, context):
        if self.variable.resolve(context) is None:
            return ""
        try:
            return str(int(self.variable.resolve(context)) + 1)
        except ValueError:
            raise template.TemplateSyntaxError("'increment tag requires a base 10 integer as parameter")

def increment(parser, token):
    parts = token.split_contents()
    if len(parts) != 2:
        raise template.TemplateSyntaxError("'increment' tag must be of form {% increment <variable> %}")
    return IncrementVariable(parts[1])


register.tag('increment', increment)
