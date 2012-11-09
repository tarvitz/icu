# -*- coding: utf-8 -*-
# code here
from django.shortcuts import redirect
from apps.banlist.models import ServerBanList
from apps.core.helpers import get_object_or_None


def owner_ban_required(field):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not field in kwargs:
                return redirect('core:blockage')
            pk = kwargs[field]
            ban = get_object_or_None(ServerBanList, pk=pk)
            if not ban:
                return redirect('core:does-not-exists')
            if ban.owner == request.user:
                return func(request, *args, **kwargs)
            return redirect('core:blockage')
        return wrapper
    return decorator
