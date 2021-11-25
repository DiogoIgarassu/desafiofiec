from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from auto_scraping.scraping import Scraping


def home(request):
    """ função para chamar a página inicial """
    return render(request, 'web/home.html')

def contact(request):
    """ função para página de contato """
    return render(request, 'web/contact.html')


def iniciar(request):
    """ função para iniciar o busca e carregamento dos dados no sistema """
    if request.method == 'POST':
        Scraping()

        return redirect('schema-swagger-ui')
    return render(request, 'web/iniciar.html')
