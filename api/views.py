from django.http import HttpResponse
from .models import Total_Comex, Products_SH6, Products_NCM, Valor_Movimentado
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import generics, permissions


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj):
            return str(obj)
        return super().default(obj)


class Total(generics.RetrieveAPIView):
    """Filtra as informações do bando pelo ano passado no url"""
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, year=None, *args):
        resultado = []
        if year:
            try:
                year = int(year)
                dados = Total_Comex.objects.filter(Ano=year)
                if dados.exists():
                    for info in dados:
                        dic = {"Total": info.Total, "Movement": info.Movement}
                        resultado.append(dic)
                else:
                    dic = {"error": f"Fora de alcance, não há dados para ano de {year}."}
                    resultado.append(dic)
            except:
                dic = {"error": "Por favor, digite um ano válido!"}
                resultado.append(dic)
        else:
            dados = Total_Comex.objects.all()
            for info in dados:
                dic = {"Total": info.Total, "Movement": info.Movement, "Year":info.Ano}
                resultado.append(dic)

        formatted_data = json.dumps(resultado, ensure_ascii=False, cls=DjangoJSONEncoder)

        return HttpResponse(formatted_data, content_type="application/json")


class Products(generics.RetrieveAPIView):
    """Filtra as informações do bando pelo ano passado no url"""
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, ncm=None, *args):
        resultado = []
        if ncm:
            try:
                NMC_NUM = int(ncm) #TESTA SE O NMC É APENAS NÚMERO
                product_NMC = Products_NCM.objects.filter(COD_NCM=ncm)

                if product_NMC.exists():
                    for info in product_NMC:
                        sh6 = info.COD_SH6_id
                        products_SH6 = Products_SH6.objects.get(id=sh6)
                        dic = {"COD_NCM": info.COD_NCM, "NM_NCM": info.NM_NCM,
                               "COD_SH2": products_SH6.COD_SH2, "NM_SH2": products_SH6.NM_SH2}
                        resultado.append(dic)
                else:
                    dic = {"error": f"Não há dados para código {ncm}."}
                    resultado.append(dic)
            except:
                dic = {"error": "Por favor, digite um código NCM válido!"}
                resultado.append(dic)
        else:
            dados = Products_NCM.objects.all()
            for info in dados:
                sh6 = info.COD_SH6_id
                products_SH6 = Products_SH6.objects.get(id=sh6)
                dic = {"COD_NCM": info.COD_NCM, "NM_NCM": info.NM_NCM,
                       "COD_SH2": products_SH6 .COD_SH2, "NM_SH2": products_SH6 .NM_SH2}
                resultado.append(dic)

        formatted_data = json.dumps(resultado, ensure_ascii=False, cls=DjangoJSONEncoder)

        return HttpResponse(formatted_data, content_type="application/json")


class Comex(generics.RetrieveAPIView):
    """Filtra as informações do bando pelo ano passado no url"""
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, movement=None, products=None, vias=None, year=None):
        resultado = []

        if movement:
            if "exp".upper() in movement.upper():
                tipo = "Exportação"
            elif "imp".upper() in movement.upper():
                tipo = "Importação"

            dados = Valor_Movimentado.objects.filter(MOVEMENT=tipo)

        if products:
            dados = dados.filter(COD_NCM=products)

        if vias:
            dados = dados.filter(COD_VIA=vias)

        if year:
            dados = dados.filter(ANO=year)

        if dados.exists():
            for info in dados:
                dic = {"VL_FOB": int(info.VL_FOB), "MONTH": int(info.MONTH), "SG_UF": info.SG_UF,
                       "COD_VIA": info.COD_VIA}
                resultado.append(dic)
        else:
            dic = {"error": f"Não há dados para valores informados."}
            resultado.append(dic)

        if not movement:
            dados = Valor_Movimentado.objects.all()[:100]
            for info in dados:
                #"Movement": info.MOVEMENT, "COD_NCM": info.COD_NCM, "ANO": info.ANO,
                dic = {"VL_FOB": int(info.VL_FOB), "MONTH": int(info.MONTH), "SG_UF": info.SG_UF,  "COD_VIA": info.COD_VIA }
                resultado.append(dic)

        formatted_data = json.dumps(resultado, ensure_ascii=False, cls=DjangoJSONEncoder)

        return HttpResponse(formatted_data, content_type="application/json")





