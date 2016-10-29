from datetime import datetime, timedelta

from tasks.models import Tarefa

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient


class BaseTestCase(TestCase):

    def setUp(self):
        self.email = 'usario@usuario.com'
        self.username = 'usuario'
        self.password = '12345'
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        self.data = {
            'username': self.username,
            'password': self.password
        } 

    def get_token(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/auth/', self.data, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data.get('token')


    def criar_tarefa(self):
        return Tarefa.objects.create(
            nome='Nome tarefa',
            descricao='Tarefa',
            inicio=datetime.now(),
            termino=datetime.now() + timedelta(days=2),
            usuario=self.user
        )


class LoginTestCase(BaseTestCase):
    def setUp(self):
        return super(LoginTestCase, self).setUp()
    
    def test_login(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/auth/', self.data, format='json')
        token = self.get_token()
        self.assertEqual(response.status_code, 200)


class TarefaTestCase(BaseTestCase):
    def setUp(self):
        return super(TarefaTestCase, self).setUp()

    def test_tarefa_ok(self):
        tarefa = {
            'nome': 'Nome tarefa',
            'descricao': 'Tarefa',
            'inicio': datetime.now(),
            'termino': datetime.now() + timedelta(days=2),
        }
        client = APIClient(enforce_csrf_checks=True)
        client.credentials(HTTP_AUTHORIZATION='jwt ' + self.get_token())
        response = client.post(
            '/tarefas/', 
            tarefa, 
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_tarefa_fail(self):
        tarefa = {
            'descricao': 'Tarefa',
            'inicio': datetime.now(),
            'termino': datetime.now() + timedelta(days=2),
        }
        client = APIClient(enforce_csrf_checks=True)
        client.credentials(HTTP_AUTHORIZATION='jwt ' + self.get_token())
        response = client.post(
            '/tarefas/', 
            tarefa, 
            format='json'
        )
        self.assertEqual(response.status_code, 400)


class TarefaEncerradaTestCase(BaseTestCase):

    def test_tarefa_encerrada(self):
        tarefa = self.criar_tarefa()
        client = APIClient(enforce_csrf_checks=True)
        client.credentials(HTTP_AUTHORIZATION='jwt ' + self.get_token())
        response = client.post(
            '/encerrada/',
            {'tarefa': tarefa.pk},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('encerrada'), True)

    def test_tarefa_reaberta(self):
        tarefa = self.criar_tarefa()
        tarefa.encerrada = True
        tarefa.save()
        client = APIClient(enforce_csrf_checks=True)
        client.credentials(HTTP_AUTHORIZATION='jwt ' + self.get_token())
        response = client.post(
            '/encerrada/',
            {'tarefa': tarefa.pk},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('encerrada'), False)



