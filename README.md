# Desafio FIEC/CE
Repositório para desafio técnico para desenvolvedor Python da FIEC/CE

Django - Docker - Celery - Redis - Beautifulsoup - API-Restful
Aplicação que minera de forma automatizada dados dos últimos 3 anos do site do Comercio Exterior do Brasil, 
baixa dos dados, popula os bancos e forncesse os dados em forma de API Django Restframework

Como rodar o projeto?

Clone esse repositório
Crie um ambiente virtualevn com python
instale as dependências
Rode as migrações

git clone https://github.com/DiogoIgarassu/desafiofiec.git
cd desafiofiec
python -m venv venv
venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

Rodando com Docker
docker-compose up --build

Rode as migrações no container
docker container exec web python manage.py migrate

Crie um super usuário
docker container exec web python manage.py createsuperuser

Entre no link para iniciar o processo automatizado de carregado dos daods
http://127.0.0.1:8000/

Após clicar em iniciar, você poderá observar no terminal do seu IDE todas as etapas do processo acontecendo
Aguarde e você será direcionado para a página do Swagger, onde em /auth/register/ você fará seu cadastro
na parte senha pode deixar "string", pois, será criada uma senha secreta e enviada para seu email.

Algumas bibliotecas python foram fundamentais para este processo

djangorestframework==3.12.4
Usada pra criar a aplicação em formato de API com Serelização dos dados 

djangorestframework-simplejwt==5.0.0
Muito importante para autenticação por token

drf-yasg==1.20.0
Cria a pagina de gerenciamento da API

beautifulsoup4==4.10.0
Permite minerar sites

celery==5.2.1
Cria um sistema de filas de atividades servidor

django-celery-beat==2.2.1
facilita o agendamento de tarefas

redis==4.0.2
mini banco utilizado para guardar as atividades em fila de execução



#COMO UTLIZAR VIA POSTMAN
Vovê deve suar o seguinte link para criar conta de usuário com método POST
http://127.0.0.1:8000/auth/register/
{
  "email": "email@email.com",
  "username": "Fulano da Silva",
  "password": "string"
}

ATENÇÃO, VOCÊ RECEBERÁ UM EMAIL COM UM LINK PARA CONFIRMAÇÃO DO CASATRO, LEMBRE-SE DE USAR UM EMAIL VÁLIDO PARA ATIVAR O CADASTRO!

você deve usar o seguinte link para login com método POST
http://127.0.0.1:8000/auth/login/
{
  "email": "email@email.com",
  "username": "Fulano da Silva"
}

Agora você receberá confirmação de login de 02 tokens, 1 de refresh e outro de access
COPIE O TOKEN DE ACCESS

Na guia Authorization, você deve escolher type: Bearer Token e colar o link que você copiou

Pronto!!

Agora só utlizar as rotas com Método GET para obter as informações desejadas.

http://127.0.0.1:8000/api/total/2021
pode pode altenar o ano de interesse

http://127.0.0.1:8000/api/products
http://127.0.0.1:8000/api/products/01019000
Possíver ver receber json com todos produtos cadastrados ou basta digitar o código NCM no final para receber dados de produtos específicos

http://127.0.0.1:8000/api/comex/exp/01019000/07/2021
agora é possível filtrar por várias variáveis, por "exp" e "imp", por código NCM, por código da Via e algum dos 3 úlimos anos.



MELHORIAS
São várias melhorias possíveis!
A primeira seria a utização dos dados para gerarem gráficos(dashboards pernonalizados) e pertmitir diversos insights, uma das minhas libs favoritas para isto é a Bokeh
Outra forma interessante é o agendamente e criação autómatica de relatórios, além a mineração diária por novos dados, estes relatórios 
poderiam ajudar na tomada de decisões de grande empresas.

