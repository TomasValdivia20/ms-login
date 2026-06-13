import os
from unittest.mock import patch

import jwt
from django.test import TestCase
from rest_framework.test import APIClient

from .services import LoginService


class LoginServiceTests(TestCase):
    @patch('login.services.httpx.post')
    def test_autenticar_y_generar_token_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'rut_empresa': '12345678-9',
            'email': 'usuario@empresa.com',
            'rol': 'admin',
            'nombre': 'Usuario Ejemplo',
        }

        os.environ['JWT_SECRET_KEY'] = 'test_secret'
        os.environ['JWT_ALGORITHM'] = 'HS256'

        resultado = LoginService.autenticar_y_generar_token('usuario@empresa.com', 'password')

        self.assertIn('access_token', resultado)
        self.assertEqual(resultado['token_type'], 'Bearer')
        self.assertEqual(resultado['usuario']['email'], 'usuario@empresa.com')

        payload = jwt.decode(
            resultado['access_token'],
            os.environ['JWT_SECRET_KEY'],
            algorithms=[os.environ['JWT_ALGORITHM']],
        )
        self.assertEqual(payload['email'], 'usuario@empresa.com')

    @patch('login.services.httpx.post')
    def test_autenticar_y_generar_token_invalid_credentials(self, mock_post):
        mock_post.return_value.status_code = 401

        with self.assertRaises(ValueError) as cm:
            LoginService.autenticar_y_generar_token('usuario@empresa.com', 'wrong')

        self.assertEqual(str(cm.exception), 'Credenciales incorrectas')

    @patch('login.services.httpx.post')
    def test_autenticar_y_generar_token_communication_error(self, mock_post):
        mock_post.side_effect = Exception('Falló la conexión')

        with self.assertRaises(RuntimeError) as cm:
            LoginService.autenticar_y_generar_token('usuario@empresa.com', 'password')

        self.assertEqual(str(cm.exception), 'Error de comunicación interna con MS-Usuario')


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/login/'

    def test_post_missing_fields_returns_400(self):
        response = self.client.post(self.url, {'email': 'usuario@empresa.com'}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Debe enviar email y password'})

    @patch('login.views.LoginService.autenticar_y_generar_token')
    def test_post_success(self, mock_login):
        mock_login.return_value = {
            'access_token': 'token123',
            'token_type': 'Bearer',
            'usuario': {'email': 'usuario@empresa.com'},
        }

        response = self.client.post(
            self.url,
            {'email': 'usuario@empresa.com', 'password': 'password'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['access_token'], 'token123')
        self.assertEqual(response.json()['usuario']['email'], 'usuario@empresa.com')

    @patch('login.views.LoginService.autenticar_y_generar_token')
    def test_post_invalid_credentials_returns_401(self, mock_login):
        mock_login.side_effect = ValueError('Credenciales incorrectas')

        response = self.client.post(
            self.url,
            {'email': 'usuario@empresa.com', 'password': 'wrong'},
            format='json',
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'error': 'Credenciales incorrectas'})
