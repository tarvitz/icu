# Create your views here.
# coding: utf-8
import os
from apps.core.helpers import render_to, ajax_response
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect


@render_to('index.html')
def index(request):
    if request.user.is_authenticated():
        return {'redirect': 'banlist:index'}
    return {}
