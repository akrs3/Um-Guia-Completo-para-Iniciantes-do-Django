from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase


from ..views import board_topics
from ..models import Board



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
    
    
    #Testando se o link de voltar para Home está pegando mesmo
    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))