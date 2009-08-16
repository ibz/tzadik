from django import template

register = template.Library()

class UrlJoinNode(template.Node):
    def __init__(self, *args):
        self.args = args

    def render(self, context):
        args = []
        for i, arg in enumerate(self.args):
            arg = arg.resolve(context)
            if i != 0 and arg.startswith("/"):
                arg = arg[1:]
            if i != len(self.args) - 1 and arg.endswith("/"):
                arg = arg[:-1]
            args.append(arg)
        return "/".join(args)

@register.tag('urljoin')
def do_urljoin(parser, token):
    args = [parser.compile_filter(a) for a in token.contents.split()[1:]]
    return UrlJoinNode(*args)
