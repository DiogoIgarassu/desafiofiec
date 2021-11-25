from celery import shared_task
from .scraping import Scraping


@shared_task(bind=True)
def scraping_func(self):
    """ função que ficará na fila e será ativada no prazo marcado """
    #Reinicia processo de mineração
    Scraping()
    return "Done"


@shared_task(bind=True)
def test_func(self):
    """ função para teste de agendamento """
    print("SE VOCÊ ESTÁ VENDO ISTO, SEU TESTE DEU CERTO XD !!!")
    return "Done"