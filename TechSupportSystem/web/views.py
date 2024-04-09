from django.shortcuts import render

def index(request):
    context = {
        'user': request.user,
    }
    return render(request, 'web/index.html', context)

def about(request):
    context = {
        'user': request.user,
    }
    return render(request, 'web/about.html', context)

def contacts(request):
    context = {
        'user': request.user,
    }
    return render(request, 'web/contacts.html', context)