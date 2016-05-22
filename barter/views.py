# Create your views here.
from django.shortcuts import render
from barter.models import XchangeStore
#from django.http import HttpResponse

def index(request):
    message = "Hi I am Binny"
    
    data_store = XchangeStore.objects.filter(category='Tools')
    
    return render(request, 'barter/index.html', {
            'question': message,
            'data_store':data_store,
            'error_message': "You didn't select a choice.",
        })

def blog(request):
    message = "It's a blog page"
    return render(request, 'barter/blog.html', { 
            'question': message,
            'error_message': "You didn't select a choice.",
        })
    