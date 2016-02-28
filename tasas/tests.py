from django.test import TestCase
from django.core.management.base import CommandError
from mock import patch, Mock, PropertyMock
from .management.commands import importar
from .models import Universidad, Tasa, CursoValidator, get_current_curso
from django.db.models import URLField
import datetime

from django.core.exceptions import ValidationError


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

class TestCursoValidator(TestCase):
    from datetime import date
    class FakeDate(date):
        """A manipulable date replacement"""
        def __new__(cls, *args, **kwargs):
            return date.__new__(date, *args, **kwargs)

    def setUp(self):
        pass

    @patch('datetime.date', FakeDate)
    def test_get_current_year(self):
        self.FakeDate.today = classmethod(lambda cls: date(2011, 1, 1))

        print(get_current_curso())

    @patch('tasas.models.datetime')
    def test_get_current_year(self, current_curso_mock):
        current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Sep 1 2011', '%b %d %Y'))
        self.assertEqual(2012, get_current_curso())

        current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Aug 31 2011', '%b %d %Y'))

        self.assertEqual(2011, get_current_curso())

    @patch('tasas.models.datetime')
    #@patch('tasas.models.settings.MIN_YEAR')
    def test_curso_validator(self, current_curso_mock):
        validator = CursoValidator()
        current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Sep 1 2011', '%b %d %Y'))

        #type(settings_mock).MIN_YEAR = PropertyMock(return_value=2011)
        #settings_mock.configure_mock(MIN_YEAR=2011)
        #settings_mock.YEARS_IN_ADVANCE = 1
        #settings_mock.CURSO_CHANGE_MONTH = 10

        self.assertRaises(ValidationError, validator.__call__(2011))

        current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Aug 1 2011', '%b %d %Y'))
        self.assertEqual(None, validator.__call__(2011))

        self.assertEqual(None, validator.__call__(2012))
        self.assertRaises(ValidationError, validator.__call__, (2013))

class TestTasaModel(TestCase):
    def setUp(self):
        pass

    def test_validator_precio_por_credito(self):
        tasa = Tasa()


        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.tipo = Tasa.PRECIO_POR_CREDITO
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.tipo_titulacion = Tasa.GRADO
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.url = "http://url.org"
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.universidad = Universidad()
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.curso = 2011

        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas1 = 10
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas2 = 20
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas3 = 30
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas4 = 40
        self.assertEqual(None, tasa.clean())

    def test_validator_precio_por_credito(self):
        tasa = Tasa()

        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.tipo = Tasa.PRECIO_POR_CREDITO
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.tipo_titulacion = Tasa.GRADO
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.url = "http://url.org"
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.universidad = Universidad()
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.curso = 2011

        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas1 = 10
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas2 = 20
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas3 = 30
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas4 = 40
        self.assertEqual(None, tasa.clean())
        tasa.tasa_global = 40
        self.assertRaises(ValidationError, tasa.clean)

    def test_validator_precio_global(self):
        tasa = Tasa()

        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.tipo = Tasa.PAGO_UNICO
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.tipo_titulacion = Tasa.GRADO
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.url = "http://url.org"
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.universidad = Universidad()
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.curso = 2011

        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasa_global = 10
        self.assertEqual(None, tasa.clean())
        tasa.tasas1 = 10
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas1 = None
        self.assertEqual(None, tasa.clean())
        tasa.tasas2 = 20
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas1 = 10
        tasa.tasas2 = 20
        self.assertRaises(ValidationError, tasa.clean)

    def test_tasa_miscelaneo(self):
        tasa = Tasa()

        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.tipo = Tasa.MISCELANEO
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.tipo_titulacion = Tasa.GRADO
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.url = "http://url.org"
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.universidad = Universidad()
        self.assertRaises(ValidationError, tasa.clean_fields)
        tasa.curso = 2011

        self.assertRaises(ValidationError, tasa.clean)
        tasa.descripcion = "Descripción"
        self.assertEqual(None, tasa.clean())

        tasa.tasas1 = 10
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas1 = None
        self.assertEqual(None, tasa.clean())
        tasa.tasas2 = 20
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas1 = 10
        tasa.tasas2 = 20
        self.assertRaises(ValidationError, tasa.clean)

        tasa.tasas1 = None
        tasa.tasas2 = None
        self.assertEqual(None, tasa.clean())

        tasa.tasa_global = 10
        self.assertRaises(ValidationError, tasa.clean)