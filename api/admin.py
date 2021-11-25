from django.contrib import admin
from .models import Total_Comex, Products_SH6, \
    Products_NCM, Via, Valor_Movimentado
# Register your models here.

admin.site.register(Total_Comex)
admin.site.register(Products_SH6)
admin.site.register(Products_NCM)
admin.site.register(Via)
admin.site.register(Valor_Movimentado)
