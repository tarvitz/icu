# coding: utf-8
from django.contrib import auth
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

class IE6BanMiddleware(object):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', 'notie')
        user = request.user
        if 'msie 6.0' in user_agent.title().lower()\
            or 'msie 5.5' in user_agent.title().lower():
            template = get_template('get_a_working_browser.html')
            out = template.render(Context())
            response = HttpResponse()
            response.write(out)
            return response
