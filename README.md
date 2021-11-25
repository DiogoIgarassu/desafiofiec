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
Vovê deve suar o seguinte link para criar conta de usuário
http://127.0.0.1:8000/auth/register/
{
  "email": "email@email.com",
  "username": "Fulano da Silva",
  "password": "string"
}


http://127.0.0.1:8000/auth/login/
