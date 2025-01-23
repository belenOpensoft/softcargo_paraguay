from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render


@login_required(login_url='/login/')
def home_view(request):
    try:
        if 'rol' in request.session:
            return render(request, 'base.html')
        else:
            return HttpResponseRedirect('/login')
    except Exception as e:
        messages.error(request,str(e))
        return render(request, 'base.html')
