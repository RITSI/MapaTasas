from django.test import TestCase
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError

from unittest import skip
from mock import patch
from django.core.files import File
from django.db.models import ImageField
from .management.commands import importar
from .models import Universidad



class TestImportarCommand(TestCase):

    def setUp(self):
        self.args = {'file':'tasas/unis.json', 'img-dir': 'img'}
        self.command = importar.Command()

    def test_invalid_data(self):

        with self.assertRaises(CommandError):
            self.command.parse_file({})
            self.command.parse_file({'unis': {}})

    #@patch.object(ImageField, 'save')
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
                self.command.add_uni(invalid_data_copy['unis'][i], 'img/uni/')

    def test_get_tipo_uni(self):
        self.assertEqual(0, self.command.get_tipo_uni("Pública"))
        self.assertEqual(1, self.command.get_tipo_uni("Privada"))
        self.assertEqual(None, self.command.get_tipo_uni(""))

class TestUniversidadModel(TestCase):

    def test_valid_strings(self):
        valid_data = (("ual", "ual"),
        ("uma", "uma"),
        ("us", "us"),
        ("upo", "upo"),
        ("uca", "uca"),
        ("uco", "uco"),
        ("uja", "uja"),
        ("uhu", "uhu"),
        ("unizar", "unizar"),
        ("usj", "usj"),
        ("ulpgc", "ulpgc"),
        ("ull", "ull"),
        ("ule", "ule"),
        ("ugr-granada", "ugr"),
        ("ugr-ceuta", "ugr"),
        ("usal-salamanca", "usal"),
        ("usal-zamora", "usal"),
        ("uva-valladolid", "uva"),
        ("uva-segovia", "uva"),
        ("uo-oviedo", "uo"),
        ("uo-gijon", "uo"))


        for data in valid_data:
            self.assertEqual(data[1], Universidad.get_siglas_no_centro(data[0]))

    def test_provincia_unicode(self):

        uni = Universidad()
        uni.provincia = 'Avila'

        self.assertEqual(uni.get_provincia_unicode(), "Ávila")