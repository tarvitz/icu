# coding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

def direct_to_template(request, template, context={},processors=[]):
    """wrapper of deprecated direct_to_template from
    django.views.generic.simple"""
    return render_to_response(template, context,
        context_instance=RequestContext(request,processors=processors))
