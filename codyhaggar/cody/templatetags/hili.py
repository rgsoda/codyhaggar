from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter
from django import template
register = template.Library()

@register.tag(name='code')
def do_code(parser,token):
    code = token.split_contents()[-1]
    nodelist = parser.parse(('endcode',))
    parser.delete_first_token()
    return CodeNode(code,nodelist)

class CodeNode(template.Node):
    def __init__(self,lang,code):
        self.lang = lang
        self.nodelist = code

    def render(self,context):
        try:
            language = template.Variable(self.lang).resolve(context)
        except:
            language = self.lang
        code = self.nodelist.render(context)
        try:
            lexer = get_lexer_by_name(language)
        except:
            try:
                lexer = guess_lexer(code)
            except:
                lexer = PythonLexer()
        formatter = HtmlFormatter(linenos=True, noclasses=True)
        return highlight(code, lexer, formatter)

