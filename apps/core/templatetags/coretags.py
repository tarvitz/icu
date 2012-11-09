# coding: utf-8
import re
import datetime
from datetime import timedelta
from django import template
from django.template import Library, Node, TemplateSyntaxError
from django.template.defaultfilters import striptags
from apps.core.helpers import get_object_or_None
from django.db.models import Q
from django.core.urlresolvers import reverse

register = Library()


class JSUrlNode(Node):
    def __init__(self, url):
        self.url = url

    def render(self, context):

        from django.core.urlresolvers import get_urlconf, get_resolver
        resolver = get_resolver(get_urlconf())
        jsurl = '/'
        if self.url in resolver.reverse_dict:
            url = resolver.reverse_dict[self.url][0][0][0]
            jsurl = re.sub(re.compile('\%(\(\w+\))\w'), '%s', url)
        return "/%(url)s" % {'url': jsurl}


@register.tag
def jsurl(parser, tokens):
    bits = tokens.contents.split()
    if len(bits) < 2:
        raise TemplateSyntaxError("jsurl takes one argument")
    url = bits[1]
    if url[1] in ('"', '"') and url[-1] in ('"', "'"):
        url = url[1:-1]
    return JSUrlNode(url)


class GetFormNode(Node):
    def __init__(self, init, varname, use_request):
        self.init = init[1:-1]
        self.varname = varname
        self.use_request = use_request

    def render(self, context):
        app = self.init[:self.init.rindex('.')]
        _form = self.init[self.init.rindex('.') + 1:]
        module = __import__(app, 0, 0, -1)
        form_class = getattr(module, _form)
        context[self.varname] = form_class(request=context['request']) \
            if self.use_request else form_class()
        return ''


@register.tag
def get_form(parser, tokens):
    bits = tokens.contents.split()
    #get_form 'apps.' for varname [use request]
    if len(bits) != 4 and len(bits) != 5:
        raise (TemplateSyntaxError,
               "get_form  'app.model.Form' for form [use_request]")
    if bits[2] != 'as':
        raise TemplateSyntaxError("the second argument must be 'as'")
    init = bits[1]
    varname = bits[3]
    use_request = bool(bits[4]) if len(bits) > 4 else False
    return GetFormNode(init, varname, use_request)


def raw(parser, token):
    # Whatever is between {% raw %} and {% endraw %} will be preserved as
    # raw, unrendered template code.
    text = []
    parse_until = 'endraw'
    tag_mapping = {
        template.TOKEN_TEXT: ('', ''),
        template.TOKEN_VAR: ('{{', '}}'),
        template.TOKEN_BLOCK: ('{%', '%}'),
        template.TOKEN_COMMENT: ('{#', '#}'),
    }
    # By the time this template tag is called, the template system has already
    # lexed the template into tokens. Here, we loop over the tokens until
    # {% endraw %} and parse them to TextNodes. We have to add the start and
    # end bits (e.g. "{{" for variables) because those have already been
    # stripped off in a previous part of the template-parsing process.
    while parser.tokens:
        token = parser.next_token()
        if (token.token_type == template.TOKEN_BLOCK
                and token.contents == parse_until):
            return template.TextNode(u''.join(text))
        start, end = tag_mapping[token.token_type]
        text.append(u'%s%s%s' % (start, token.contents, end))
    parser.unclosed_block_tag(parse_until)
raw = register.tag(raw)


class CheckLocationNode(Node):
    def __init__(self, url, varname):
        self.url = url
        self.out = varname[1:-1]

    def render(self, context):
        full_path = context.get('get_full_path', '')
        if full_path == reverse(self.url):
            return self.out
        return ''


@register.tag
def check_location(parser, tokens):
    bits = tokens.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError("check_location reverse_url as 'var'")
    if bits[2] != 'as':
        raise TemplateSyntaxError("the second argument must be 'as'")
    url = bits[1]
    out = bits[3]
    return CheckLocationNode(url, out)
