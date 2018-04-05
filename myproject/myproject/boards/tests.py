from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from .views import home, board_topics
from .models import Board


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
        view = resolve('/') #garante q o url / que é o raiz retorne a view home
        self.assertEquals(view.func, home)

    #método assertContains para testar se o corpo da resposta contém um determinado texto
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
    #no metodo setup preparamos o ambiente p execucao dos testes, simular o cenario
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    #Testando se o codigo de status da resposta e 200 (sucesso) ou nao
    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    #Testando se o codigo de status da resposta e 404 (erro de pagina n encontrada) ou nao
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    #Testando se Django esta retornando a view correta na chamada do url
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))