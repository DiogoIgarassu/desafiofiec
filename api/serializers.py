from rest_framework import serializers
from api.models import Total_Comex, Products_NCM, Valor_Movimentado


class TotalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Total_Comex
        fields = '__all__'


class ProductsNCMSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products_NCM
        fields = '__all__'


class ValorMovimentadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Valor_Movimentado
        fields = '__all__'