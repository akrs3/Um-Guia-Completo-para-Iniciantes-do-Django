from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

from ..views import home
from ..models import Board
from ..views import BoardListView

class HomeTests(TestCase):
    
    #no metodo setup preparamos o ambiente p execucao dos testes, simular o cenario
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    #Testando o codigo de status da resposta
    #200 e o codigo de sucesso, se houvesse alguma excecao o Django retornaria um codigo 500
    def test_home_view_status_code(self):
        #url = reverse('home')
        #response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    #Testando se Django esta retornando a view correta na chamada do url
    def test_home_url_resolves_home_view(self):
        '''view = resolve('/') #garante q o url / que é o raiz retorne a view home
        self.assertEquals(view.func, home)'''
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)

    #método assertContains para testar se o corpo da resposta contém um determinado texto
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
