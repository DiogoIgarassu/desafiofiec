from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    return render(request, 'web/home.html')

def contact(request):
    return render(request, 'web/contact.html')

