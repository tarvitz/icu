# Create your views here.
from apps.core.helpers import render_to, get_object_or_None, get_object_or_404

from apps.banlist.models import ServerBanList
from apps.banlist.forms import AddServerBanForm
from apps.banlist.decorators import owner_ban_required

from django.contrib.auth.decorators import login_required


@login_required
@render_to('banlist/index.html')
def index(request):
    users = []
    servers = ServerBanList.objects.filter(owner=request.user)
    form = AddServerBanForm()
    return {'servers': servers, 'users': users, 'form': form}


@login_required
@render_to('banlist/add.html')
def add(request, pk=None):
    instance = get_object_or_None(ServerBanList, pk=pk)
    form = AddServerBanForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            ban = form.save(commit=False)
            ban.owner = request.user
            ban.save()
            return {'redirect': 'banlist:index'}
    return {
        'form': form
    }


@login_required
@owner_ban_required(field='pk')
def edit(request, pk):
    instance = get_object_or_404(ServerBanList, pk=pk)
    return add(request, pk=pk)


@login_required
@owner_ban_required(field='pk')
@render_to('banlist/delete.html')
def delete(request, pk):
    instance = get_object_or_404(ServerBanList, pk=pk)
    instance.delete()
    return {'redirect': 'banlist:index'}
