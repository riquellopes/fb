# coding: utf-8
import unittest
import responses
# from nose.tools import assert_equals
from app import app


class App(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @responses.activate
    def test_1(self):
        """
            Caso o usuário /1 seja recuperado, o nome dele deve ser henrique lopes
        """
        json = ''
        responses.add(responses.GET, 'URL',
                      body=json,
                      status=200,
                      content_type="application/json")

        # response = self.app("/1")
