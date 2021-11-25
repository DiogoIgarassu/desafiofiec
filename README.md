# Desafio FIEC/CE
Repositório para desafio técnico para desenvolvedor Python da FIEC/CE

Django - Docker - Celery - Redis - Beautifulsoup - API-Restful
Aplicação que minera de forma automatizada dados dos últimos 3 anos do site do Comercio Exterior do Brasil, 
baixa dos dados, popula os bancos e forncesse os dados em forma de API Django Restframework

<h2>Como rodar o projeto?</h2>

<h3>Clone esse repositório</h3>
<ol>
<li> Crie um ambiente virtualevn com python</li>
<li> Instale as dependências</li>
<li> Rode as migrações</li>
</ol>

```
[x] git clone https://github.com/DiogoIgarassu/desafiofiec.git<br>
[x] cd desafiofiec<br>
[x] python -m venv venv<br>
[x] venv/scripts/activate<br>
[x] pip install -r requirements.txt<br>
[x] python manage.py migrate<br>
```

<h3> Rodando com Docker </h3>
<b>docker-compose up --build</b>

<h3>Rode as migrações no container</h3>
<b>docker container exec web python manage.py migrate</b>

<h3>Crie um super usuário</h3>
<b>docker container exec web python manage.py createsuperuser</b>

<h4>Entre no link para iniciar o processo automatizado de carregado dos daods</h4>
http://127.0.0.1:8000/

<br>Após clicar em iniciar, você poderá observar no terminal do seu IDE todas as etapas do processo acontecendo
Aguarde e você será direcionado para a página do Swagger, onde em /auth/register/ você fará seu cadastro
na parte senha pode deixar "string", pois, será criada uma senha secreta e enviada para seu email.

<h3>Algumas bibliotecas python foram fundamentais para este processo</h3>

<b>djangorestframework==3.12.4</b>
<br>Usada pra criar a aplicação em formato de API com Serelização dos dados 

<b>djangorestframework-simplejwt==5.0.0</b>
<br>Muito importante para autenticação por token

<b>drf-yasg==1.20.0</b>
<br>Cria a pagina de gerenciamento da API

<b>beautifulsoup4==4.10.0</b>
<br>Permite minerar sites

<b>celery==5.2.1</b>
<br>Cria um sistema de filas de atividades servidor

<b>django-celery-beat==2.2.1</b>
<br>facilita o agendamento de tarefas

<b>redis==4.0.2</b>
<br>mini banco utilizado para guardar as atividades em fila de execução


<h2>COMO UTLIZAR VIA POSTMAN</h2>
Vovê deve suar o seguinte link para criar conta de usuário com método <b>POST</b>
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

Na guia Authorization, você deve escolher type: Bearer Token e colar o link que você copiou

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
<li>A primeira seria a utização dos dados para gerarem gráficos(dashboards pernonalizados) e pertmitir diversos insights, uma das minhas libs favoritas para isto é a Bokeh.</li>
<li>Outra forma interessante é o agendamente e criação autómatica de relatórios, além a mineração diária por novos dados, estes relatórios 
poderiam ajudar na tomada de decisões de grande empresas.</li>
</ol>
