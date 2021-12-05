# Desafio FIEC/CE
Repositório para desafio técnico para desenvolvedor Python da FIEC/CE

Django - Docker - Celery - Redis - Beautifulsoup - API-Restful
Aplicação que minera de forma automatizada dados dos últimos 3 anos do site do Comercio Exterior do Brasil, 
baixando os dados, populando os banco e fornecendo os dados em forma de API Django Restframework

<h2>Como rodar o projeto?</h2>

<h3>Clone esse repositório</h3>
<ol>
<li> Crie um ambiente virtual com python</li>
<li> Ative o ambiente virtual</li>
<li> Inicie o docker</li>
</ol>

```
[x] Abra o cmd, shell ou IDE na pasta de preferência para o projeto e use os comandos:
[x] git clone https://github.com/DiogoIgarassu/desafiofiec.git
[x] cd desafiofiec
[x] python -m venv venv
[x] venv\scripts\activate
```

<h3> Rodando com Docker </h3>
<b>docker-compose up --build</b>

<h3>AVISO:</h3>
<b>se passar mais de 10 minutos e não aparecer a frase "Starting development server at http://0.0.0.0:8000/", você deve pressionar  Ctrl + C e repetir o comando anterior</b>


<h4>Entre no link para iniciar o processo automatizado de busca e carregamento dos dados</h4>
http://localhost:8000/

<br> Haverá algumas opções na página inicial, você deve criar em "Iniciar Sistema" e na próxima página clicar no botão vermelho em "Iniciar Sistema"

<br><b>AVISO:</b>
<br>Você pode iniciar o sistema para testes (carregando parte dos arquivos CSV) ou comentar com # as linhas 145, 146 e 240 do arquivo /desafiofiec/auto_scraping/scraping.py para que seja carregadas todas as milhões de linhas de informações dos arquivos CSV no banco de dados.

<br>Após clicar em iniciar, você poderá observar no terminal do seu IDE todas as etapas do processo acontecendo.
<br>Aguarde e você será direcionado para a página do Swagger, onde no ENDPOINT /auth/register/ você fará seu cadastro,
na parte senha pode deixar "string", pois, será criada uma senha secreta e enviada para seu email válido.

<br><b>Observação:</b>
<br>Caso não for direcionado automaticamente para o swagger você poderá voltar a página inicial e clicar em "Gerenciamento da API"

<h3>Crie um super usuário para acessar o painel administrativo do Django e ver os dados do banco</h3>
<b>docker-compose run web python manage.py createsuperuser</b>
<br>acessar o link: http://localhost:8000/admin

<h3>Algumas bibliotecas python foram fundamentais para este processo</h3>

<b>Django==3.2.9</b>
<br>Um framework python completo que permite um ganho de produtividade por seu design pattern MVT(Model-View-Template) architecture.

<b>djangorestframework==3.12.4</b>
<br>Usada pra criar a aplicação em formato de API com Serelização dos dados 

<b>djangorestframework-simplejwt==5.0.0</b>
<br>Usada para autenticação por token

<b>drf-yasg==1.20.0</b>
<br>Cria a pagina swagger de gerenciamento da API

<b>beautifulsoup4==4.10.0</b>
<br>Permite minerar sites navegando nas tags HTML

<b>celery==5.2.1</b>
<br>Cria um sistema de filas de atividades agendadas pelo servido

<b>django-celery-beat==2.2.1</b>
<br>facilita o agendamento de tarefas com funções pré definidas

<b>redis==4.0.2</b>
<br>mini banco utilizado para guardar as atividades em fila de execução


<h2>COMO UTLIZAR VIA POSTMAN</h2>
Vovê deve usar o seguinte link para criar conta de usuário com método <b>POST</b>
<br>http://127.0.0.1:8000/auth/register/

```
{
  "email": "email@email.com",
  "username": "Fulano da Silva",
  "password": "string"
}
```
<b>ATENÇÃO, VOCÊ RECEBERÁ UM EMAIL COM UM LINK PARA CONFIRMAÇÃO DO CASATRO, LEMBRE-SE DE USAR UM EMAIL VÁLIDO PARA ATIVAR O CADASTRO!</b>

você deve usar o seguinte link para login com método POST
<br>http://127.0.0.1:8000/auth/login/
```
{
  "email": "email@email.com",
  "username": "Fulano da Silva"
}
```

Agora você receberá confirmação de login de 02 tokens, 1 de refresh e outro de access
<b>COPIE O TOKEN DE ACCESS</b>

<b>Na guia Authorization, você deve escolher type: Bearer Token e colar o link que você copiou</b>

Pronto!!

Agora só utlizar as rotas com <b>Método GET</b> para obter as informações desejadas.

<br>http://127.0.0.1:8000/api/total/2021
<br>pode pode altenar o ano de interesse

<br>http://127.0.0.1:8000/api/products
<br>http://127.0.0.1:8000/api/products/01019000
<br>Possíver ver receber json com todos produtos cadastrados ou basta digitar o código NCM no final para receber dados de produtos específicos

<br>http://127.0.0.1:8000/api/comex/exp/01019000/07/2021
<br>agora é possível filtrar por várias variáveis, por "exp" e "imp", por código NCM, por código da Via e algum dos 3 úlimos anos.



<h2>MELHORIAS</h2>
<h3>São várias melhorias possíveis!</h3>
<ol>
<li>A primeira seria a utilização dos dados para gerarem gráficos(dashboards pernonalizados) e pertmitir diversos insights, uma das minhas libs favoritas para isto é a Bokeh.</li>
<li>Outra forma interessante é o agendamente e criação autómatica de relatórios, além a mineração diária por novos dados, estes relatórios 
poderiam ajudar na tomada de decisões de grande empresas.</li>
<li>User biblioteca pandas para transformar os arquivos CSV em matrizes dataframe e assim com menos linhas de progração manipular os dados e popular o banco.</li>
</ol>
