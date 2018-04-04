from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from .views import home



class HomeTests(TestCase):
    
    #Testando o codigo de status da resposta
    #200 e o codigo de sucesso, se houvesse alguma excecao o Django retornaria um codigo 500
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    #Testando se Django esta retornando a view correta na chamada do url
    def test_home_url_resolves_home_view(self):
        view = resolve('/') #garante q o url / que é o raiz retorne a view home
        self.assertEquals(view.func, home)

