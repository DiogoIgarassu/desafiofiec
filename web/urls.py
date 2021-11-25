from web.views import *
from django.urls import path, include

app_name = 'core'
urlpatterns = [
    path('', home, name='home'),
    path('iniciar', iniciar, name='iniciar'),
    path('contato/', contact, name='contact'),
]
