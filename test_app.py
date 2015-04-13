# coding: utf-8
import unittest
import responses
from mock import patch
from nose.tools import assert_equals
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.application.config['TEST'] = True
        self.app.application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    @responses.activate
    @patch('app.db.session.commit')
    def test_1(self, c):
        """
            Caso o usuário /1 seja recuperado, o nome dele deve ser henrique lopes
        """
        json = '{"username":"henrique", "id":1, "name":"lopes", "gender":"male"}'
        url = self.app.application.config['GRAPH_FB'].format(1)
        responses.add(responses.GET, url,
                      body=json,
                      status=200,
                      content_type="application/json")

        response = self.app.post("/person/", data={"facebookid": 1})
        assert_equals(response.status, '201 CREATED')
