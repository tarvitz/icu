# coding: utf-8
import re
from apps.core.helpers import generate_safe_value, get_object_or_None
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import redirect

def void_view_old(func):
    def wrapper(*args, **kwargs):
        return HttpResponse('void')
    return wrapper

def lock_with_demo(func):
    def wrapper(request, **kwargs):
        if hasattr(settings,'DEMO'):
            if settings.DEMO:
                return HttpResponseRedirect(reverse('url_demo_restrictions'))
        return func(request, **kwargs)
    return wrapper

def lock(param):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if hasattr(settings, param):
                if getattr(settings, param):
                    return func(request, *args, **kwargs)
            return redirect('core:blockage')
        return wrapper
    return decorator

def check_allowed(*args):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            for key in args:
                try:
                    value = getattr(settings, key)
                    if not value:
                        return HttpResponseRedirect(reverse('url_blockage'))
                except:
                    pass
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def void_xhr(func):
    def wrapper(request, *args, **kwargs):
        if 'type' in kwargs:
            type = kwargs['type']
            if type == 'void':
                response = HttpResponse()
                response['Content-Type'] = 'text/javascript'
                response.write('[]')
        return func(request, *args, **kwargs)
    return wrapper

def void_view(type, field):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if field in kwargs:
                if kwargs[field] == type:
                    return HttpResponseRedirect(reverse('url_index'))
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def validate_get_params(parse_dict):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            request._safe_GET = {}
            safe_value = None
            for key in parse_dict.keys():
                value = request.GET.get(key, None)
                safe_value = generate_safe_value(value, parse_dict[key])
                if safe_value is not None:
                    request._safe_GET.update({key: safe_value})
            if request._safe_GET:
                request.SAFE_GET = request._safe_GET
            delattr(request, '_safe_GET')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def comment_owner_required(field):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            from apps.core.models import Comment
            comment_id = kwargs[field]
            comment = get_object_or_None(Comment, id=comment_id)
            user = comment.author if comment else None
            if user == request.user:
                return func(request, *args, **kwargs)
            return HttpResponseRedirect(reverse('url_permission_denied'))
        return wrapper
    return decorator

def check_xhr_secure(func):
    def wrapper(request, sid, **kwargs):
        session = get_object_or_None(XHRSession, pk=sid)
        if not session:
            return func(request, sid, **kwargs)
        if not session.is_secure or (session.is_secure and session.owner == request.user):
            return func(request, sid, **kwargs)
        response = HttpResponse()
        response['Content-Type'] = 'text/javascript'
        response.write('[]')
        return response
    return wrapper

def xhr_session(func):
    """ writes response to database response marked as text/javascript
    or text/json
    the part of bullet-proof ajax handling
    """
    def wrapper(request, *args, **kwargs):
        """ depends on xhrsid with POST or GET keyword """
        if 'xhrsid' in request.GET or 'xhrsid' in request.POST:
            xhrsid = request.POST.get('xhrsid') or request.GET.get('xhrsid')
            response = func(request, *args, **kwargs)
            if response.status_code == 200:
                #only json and javascript is allowed, not html or something else
                content_type = response.get('Content-Type', 'text/html')
                if re.match(re.compile(r'text/[javascript|json]'), content_type):
                    write_xhr_session(response.content, xhrsid)
                return response
        #action by default
        return func(request, *args, **kwargs)
    return wrapper

def login_required_json(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        response = HttpResponse()
        response['Content-Type'] = 'text/javascript'
        response.write('{"success": false, "error": "login requried"}')
        return response
    return wrapper

def check_cross_domain(func):
    """
    allows complete cross domain js if owner registered an application
    domain must contain domain name without proto
    (http/https allowed via autodetection)
    proto automatically resolved via referer of passes to http as safty-default
    """
    def wrapper(request, *args, **kwargs):
        appid = request.POST.get('appid', request.GET.get('appid', None))
        if not appid:
            return func(request, *args, **kwargs)
        app = get_object_or_None(WebApp, id=appid)
        if not app:
            return func(request, *args, **kwargs)
        response = func(request, *args, **kwargs)
        proto = request.META.get('HTTP_ORIGIN', '')
        m = re.match(re.compile('http[s]'), proto)
        proto = m.group() if m else 'http'
        response['Access-Control-Allow-Origin'] = '%(proto)s://%(domain)s' % {
            'domain': app.domain,
            'proto': proto
        }
        return response
    return wrapper
