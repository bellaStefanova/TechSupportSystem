from django.shortcuts import render

# TODO: make FBV to CBV
def index(request):
    return render(request, 'web/index.html')

def about(request):
    return render(request, 'web/about.html')

def contacts(request):
    return render(request, 'web/contacts.html')