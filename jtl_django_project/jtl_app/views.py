from django.http import HttpResponse
from django.shortcuts import render

from .models import Jump, Jumper

def index(request):
    return HttpResponse("Hello, mate. You're at the JTL index.")

def jumpers(request):
    jumper_list = Jumper.objects.order_by('name')
    context = {
        'jumper_list': jumper_list,
    }
    return render(request, 'jtl_app/jumpers.html', context)

def jumps(request, jumper_id):
    jump_list = Jump.objects.filter(jumper_id_id=jumper_id)
    context = {
        'jump_list': jump_list,
    }
    return render(request, 'jtl_app/jumps.html', context)
