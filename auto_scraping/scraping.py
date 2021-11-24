import os
import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
from collections import defaultdict
from api.models import Total_Comex, Products_SH6, Products_NCM, Via, Valor_Movimentado
import time


start = time.time()
ANO_ATUAL = 0

def tempo():
    end = time.time()
    total = (end - start)
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    print('Este processo demorou {:.1f} hora(s), {:.1f} minutos e {:.1f} segundos.'.format(h, m, s))
    print('Obrigado por sua preferência XD !!!')


def create_file_search_list():
    global ANO_ATUAL
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    year = int(year)
    ANO_ATUAL = year
    NAME_FILES = ['EXP_TOTAIS_CONFERENCIA', 'NCM', 'NCM_SH','IMP_TOTAIS_CONFERENCIA',  'VIA']
    print("Criando lista de arquivos com informações dos últimos 03 anos a serem baixados...")
    for i in range(0, 3):
        NAME_FILES.append(f'EXP_{year}')
        NAME_FILES.append(f'IMP_{year}')
        year -= 1
    return NAME_FILES


def baixar_arquivo(url, endereco):
    # faz requisição ao servidor
    resposta = requests.get(url, verify=False)
    if resposta.status_code == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
            novo_arquivo.write(resposta.content)
        print("Donwload finalizado. Salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()


def Scraping():
    global start
    start = time.time()
    print(f"iniciando o processo em {time.ctime()}")

    urllib3.disable_warnings()
    url = 'https://www.gov.br/produtividade-e-comercio-exterior/pt-br/assuntos/comercio-exterior/estatisticas/base-de-dados-bruta'

    headers = {'User-Agente': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}

    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    dados = soup.find_all('table', class_="plain")
    NAME_FILES = create_file_search_list()
    BASE_URL = defaultdict(list)
    print("Minerando site do Comércio Exterior...")

    for linha in dados:
        links = linha.find_all('a')
        for link in links:
            href = link.get('href')
            href_list = href.split('/')
            name_file = href_list[-1][:-4]
            if name_file in NAME_FILES:
                BASE_URL[name_file] = href

    print("Todos os links para download coletados...")
    OUTPUT_DIR = 'BASE_DADOS'

    for file in BASE_URL:
        print(f"Iniciando o download do arquivo {file}.csv, por favor, aguarde!")
        nome_arquivo = os.path.join(OUTPUT_DIR, f'{file}.csv')
        baixar_arquivo(BASE_URL[file], nome_arquivo)

    print(f'foram baixados ao todo {len(BASE_URL)} arquivos...')
    inserir_total(NAME_FILES)


def inserir_total(NAME_FILES):
    print("Ininicando a inserção de dados no banco de dados...")
    NAME_FILES = NAME_FILES
    LISTA_TOTAIS = []
    for name in NAME_FILES:
        if "TOTAIS" in name:
            LISTA_TOTAIS.append(name)
            del (NAME_FILES[NAME_FILES.index(name)])
    print("Inserindo arquivos com valores totais por movimentação...")
    for total in LISTA_TOTAIS:
        dados_totais = open(f'./BASE_DADOS/{total}.csv').readlines()
        lista_anos = list()
        for i in range(len(dados_totais)):
            linha = dados_totais[i].strip().replace('"', '')
            linha = linha.split(';')
            if i != 0:
                ano = int(linha[1])
                lista_anos.append(ano)
                try:
                    if 'EXP' in linha[0]:
                        total_comex = Total_Comex.objects.create(Nome_Arquivo=linha[0], Movement="Exportação",
                                                                 Ano=ano, Total=linha[4])
                        total_comex.save()
                except:
                    print(f"Não foi possível inserir a linha {i}")
                try:
                    if 'IMP' in linha[0]:
                        total_comex = Total_Comex.objects.create(Nome_Arquivo=linha[0], Movement="Importação",
                                                                 Ano=ano, Total=linha[4])
                        total_comex.save()
                except:
                    print(f"Não foi possível inserir a linha {i}")

    print("ok, etapa concluída, agora preparando para inserir os dados de produtos...")
    inserir_products(NAME_FILES)


def inserir_products(NAME_FILES):
    NAME_FILES = NAME_FILES
    ARQUIVO_NCM = 'NCM'
    ARQUIVO_NCM_SH = 'NCM_SH'
    del(NAME_FILES[NAME_FILES.index(ARQUIVO_NCM)])
    del (NAME_FILES[NAME_FILES.index(ARQUIVO_NCM_SH)])
    dados_NCM = open(f'./BASE_DADOS/{ARQUIVO_NCM}.csv').readlines()
    dados_NCM_SH = open(f'./BASE_DADOS/{ARQUIVO_NCM_SH}.csv').readlines()
    contador = 0
    total_NCM = len(dados_NCM)
    total_NCM_SH = len(dados_NCM_SH)
    total_NCM = 1000 #APAGAR, APENAS PARA TESTE
    total_NCM_SH = 1000 #APAGAR, APENAS PARA TESTE

    for i in range(total_NCM_SH):
        linha = dados_NCM_SH[i].strip().replace('"','')
        linha = linha.split(';')
        if i == 0:
            demominador = round(total_NCM_SH / 100)
            print(f"Inserindo {total_NCM_SH } linhas de dados do arquivo {ARQUIVO_NCM_SH}.csv.")
            title = linha
            CO_SH6 = title.index("CO_SH6")
            CO_SH2 = title.index("CO_SH2")
            NO_SH2 = title.index("NO_SH2_POR")

        if i != 0:
            try:
                products_SH6 = Products_SH6.objects.create(COD_SH6=linha[CO_SH6], COD_SH2=linha[CO_SH2], NM_SH2=linha[NO_SH2])
                products_SH6.save()
                contador += 1
                if i % demominador == 0:
                    porcent = (i / demominador)
                    print(f'{porcent}% concluído')
            except:
                print(f"Não foi possível inserir a linha {i}")

    for i in range(total_NCM):
        linha = dados_NCM[i].strip().replace('"','')
        linha = linha.split(';')
        if i == 0:
            demominador = round(total_NCM / 100)
            print(f"Inserindo {total_NCM} linhas de dados do arquivo {ARQUIVO_NCM}.csv.")
            title = linha
            CO_NCM = title.index("CO_NCM")
            NO_NCM = title.index("NO_NCM_POR")
            CO_SH6 = title.index("CO_SH6")
            contador += 1
        if i != 0:
            try:
                SH6 = Products_SH6.objects.get(COD_SH6=linha[CO_SH6])
                products_NCM = Products_NCM.objects.create(COD_SH6=SH6, COD_NCM=linha[CO_NCM], NM_NCM=linha[NO_NCM])
                products_NCM.save()
                if i % demominador == 0:
                    porcent = (i / demominador)
                    print(f'{porcent}% concluído')
            except:
                print(f"Não foi possível inserir a linha {i}")

    print(f"Ao todos foram inseridas {contador} linhas de dados com sucesso!")
    print("Preparando para próxima etapa, o processo está correndo muito bem... ")
    inserir_via(NAME_FILES)


def inserir_via(NAME_FILES):
    NAME_FILES = NAME_FILES
    ARQUIVO_VIA = 'VIA'
    del (NAME_FILES[NAME_FILES.index(ARQUIVO_VIA)])
    dados_VIA = open(f'./BASE_DADOS/{ARQUIVO_VIA}.csv').readlines()
    contador = 0
    total_VIA = len(dados_VIA)

    for i in range(total_VIA):
        linha = dados_VIA[i].strip().replace('"','')
        linha = linha.split(';')
        if i == 0:
            demominador = round(total_VIA / 100)
            print(f"Inserindo {total_VIA } do {ARQUIVO_VIA}.")
            title = linha
            CO_VIA = title.index("CO_VIA")
            NO_VIA = title.index("NO_VIA")

        if i != 0:
            try:
                via = Via.objects.create(COD_VIA=linha[CO_VIA], NM_VIA=linha[NO_VIA])
                via.save()
                contador += 1
                if i % demominador == 0:
                    porcent = (i / demominador)
                    print(f'{porcent}% concluído')
            except:
                print(f"Não foi possível inserir a linha {i}")

    print("Ok, chegamos na parte mais demorada, boa sorte pro seu PC :p hahaha, relaxe!!")
    print("Agora serão inseridos so arquivos com valor movimentado por tipo de movimentação, produtos, via e ano...")
    inserir_movimentacoes(NAME_FILES)


def inserir_movimentacoes(NAME_FILES):
    NAME_FILES = NAME_FILES

    for ARQUIVO in NAME_FILES:
        dados_moviments = open(f'./BASE_DADOS/{ARQUIVO}.csv').readlines()
        contador = 0
        total_linhas = len(dados_moviments)
        total_linhas = 1000  #APAGAR ESTA LINHA NO PROJETO EM PRODUÇÃO

        for i in range(total_linhas):
            linha = dados_moviments[i].strip().replace('"','')
            linha = linha.split(';')

            if i == 0:
                demominador = round(total_linhas / 100)
                print(f"Inserindo {total_linhas } linhas de dados do arquivo {ARQUIVO}.csv")
                title = linha
                CO_ANO = title.index("CO_ANO")
                CO_MES = title.index("CO_MES")
                CO_NCM = title.index("CO_NCM")
                SG_UF_NCM = title.index("SG_UF_NCM")
                CO_VIA = title.index("CO_VIA")
                VL_FOB = title.index("VL_FOB")
                if "EXP" in ARQUIVO:
                    MOVEMENT = "Exportação"
                else:
                    MOVEMENT = "Importação"

            if i != 0:
                try:
                    movement = Valor_Movimentado.objects.create(ANO=linha[CO_ANO], MONTH=linha[CO_MES],
                                                                COD_NCM=linha[CO_NCM], SG_UF=linha[SG_UF_NCM],
                                                                COD_VIA=linha[CO_VIA], VL_FOB=linha[VL_FOB],
                                                                MOVEMENT=MOVEMENT)
                    movement.save()
                    contador += 1
                    if i % demominador == 0:
                        porcent = (i / demominador)
                        print(f'{porcent}% concluído')
                except:
                    print(f"Não foi possível inserir a linha {i}")

    print(f"Obrigado pela paciência, se você chegou aqui a operação foi um sucesso!!!")
    tempo()

