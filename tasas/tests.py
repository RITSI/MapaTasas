from django.test import TestCase
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError

from unittest import skip

from .management.commands import importar



class TestImportarCommand(TestCase):
    def setUp(self):
        self.args = {'file':'tasas/unis.json', 'img-dir': 'img'}
        self.command = importar.Command()
    def test_invalid_data(self):

        with self.assertRaises(CommandError):
            self.command.parse_file({})
            self.command.parse_file({'unis': {}})

    def test_null_keys(self):
        invalid_data ={'unis':
                           [{"siglas": "ual",
                            "nombre": "Universidad de Almería",
                            "tipo": "Pública",
                            "centro": "Escuela Superior de Ingeniería",
                            "provincia": "Almeria"}]}

        for i in range(0, len(invalid_data.get('unis'))):
            invalid_data_copy = invalid_data.copy()
            for key in invalid_data_copy['unis'][i].keys():
                invalid_data_copy['unis'][i][key] = ''

            with self.assertRaises(ValidationError):
                self.command.add_uni(invalid_data_copy['unis'][i])

    def test_get_tipo_uni(self):
        self.assertEqual(0, self.command.get_tipo_uni("Pública"))
        self.assertEqual(1, self.command.get_tipo_uni("Privada"))
        self.assertEqual(None, self.command.get_tipo_uni(""))