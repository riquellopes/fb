# coding: utf-8
import unittest
import responses
# from flask.ext.testing import TestCase
# from mock import patch
import json
from nose.tools import assert_equals
from app import app, Person, db


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.application.config['TEST'] = True
        self.app.application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    @responses.activate
    def test_1(self):
        """
            Caso um cadastro seja realizado, a aplicaçaõ deve recuperar status 201.
        """
        json = '{"username":"henrique", "id":1, "name":"lopes", "gender":"male"}'
        url = self.app.application.config['GRAPH_FB'].format(1)
        responses.add(responses.GET, url,
                      body=json,
                      status=200,
                      content_type="application/json")

        response = self.app.post("/person/", data={"facebookid": 1})
        assert_equals(response.status, '201 CREATED')

    def test_2(self):
        """
            Caso usuário /person/1 seja removido, aplicação deve retorna o status 204.
        """
        response = self.app.delete("/person/1")
        assert_equals(response.status, '204 NO CONTENT')

    def test_3(self):
        """
            Caso o serviço /person/ seja chamando, ele deve devolver a lista completa
            de usuarios.
        """
        p = Person(**{
            'username': "jonas",
            'facebookId': 1,
            'name': 'jonas',
            'gender': 'hominho'
        })
        db.session.add(p)
        db.session.commit()
        response = self.app.get("/person/")
        assert_equals(response.status, '200 OK')
        data = json.loads(response.data)
        assert_equals(len(data), 1)

    def test_4(self):
        """
            Caso o serviço /person/?limit=1 seja passado como parametro, o serviço deve
            limtar o tamanho da resposta.
        """
        p1 = Person(**{
            'username': "jonas",
            'facebookId': 2,
            'name': 'jonas',
            'gender': 'hominho'
        })
        p2 = Person(**{
            'username': "jonas",
            'facebookId': 3,
            'name': 'jonas',
            'gender': 'hominho'
        })
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        response = self.app.get("/person/?limit=2")
        assert_equals(response.status, '200 OK')
        data = json.loads(response.data)
        assert_equals(len(data), 2)
