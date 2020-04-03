from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.management.base import CommandError

from mock import patch
from .forms import UniversidadForm
from .management.commands import importar
from .models import Universidad, Tasa, Curso  # CursoValidator, get_current_curso, curso_choices


class TestImportarCommand(TestCase):

    def setUp(self):
        self.args = {'file':'tasas/unis.json', 'img-dir': 'img'}
        self.command = importar.Command()

    def test_invalid_data(self):

        with self.assertRaises(CommandError):
            self.command.parse_file({})
            self.command.parse_file({'unis': {}})

    # @patch.object(ImageField, 'save')
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

    def test_get_importar_uni(self):
        uni = Universidad()
        uni.nombre = "Nombre_uni"
        uni.siglas = "sigla"
        uni.provincia = "Avila"
        uni.tipo = Universidad.PUBLICA
        uni.save()
        data = {"tasas_2011": {
                "url": "",
                "tasas1": "20.29",
                "tasas2": "26.38",
                "tasas3": "30.44",
                "tasas4": ""
                },
                "tasas_2012": {
                    "url": "",
                    "tasas1": "20.89",
                    "tasas2": "28.90",
                    "tasas3": "54.32",
                    "tasas4": "75.21"
                },
                "tasas_2013": {
                    "url": "http://www.boe.es/boe/dias/2013/08/08/pdfs/BOE-A-2013-8800.pdf",
                    "tasas1": "21.24",
                    "tasas2": "29.74",
                    "tasas3": "55.24",
                    "tasas4": "76.48"
                },
                "tasas_2014": {
                    "url": "http://www.boe.es/boe/dias/2014/08/07/pdfs/BOE-A-2014-8552.pdf",
                    "tasas1": "22.00",
                    "tasas2": "30.00",
                    "tasas3": "65.00",
                    "tasas4": "90.00"
                },
                "tasas_2015": {
                    "url": "http://www.bocm.es/boletin/CM_Orden_BOCM/2015/08/03/BOCM-20150803-15.PDF",
                    "tasas1": "27.90",
                    "tasas2": "51.42",
                    "tasas3": "96.43",
                    "tasas4": "128.57"
                }}

        self.command.add_tasas(data,uni)


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
                      ("uc3m", "uc3m"),
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
    class FakeDate(date):
        """A manipulable date replacement"""
        def __new__(cls, *args, **kwargs):
            return date.__new__(date, *args, **kwargs)

    def setUp(self):
        pass

    @patch('datetime.date', FakeDate)
    def test_get_current_year(self):
        self.FakeDate.today = classmethod(lambda cls: date(2011, 1, 1))

    # TODO: Volver a activar cuando volvamos a tener una gestión automática de cursos.
    # @patch('tasas.models.datetime')
    # def test_get_current_year(self, current_curso_mock):
    #     current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Sep 1 2011', '%b %d %Y'))
    #     self.assertEqual(2011, get_current_curso())
    #
    #     current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Aug 31 2011', '%b %d %Y'))
    #
    #     self.assertEqual(2010, get_current_curso())
    #
    # @patch('tasas.models.datetime')
    # #@patch('tasas.models.settings.MIN_YEAR')
    # def test_curso_validator(self, current_curso_mock):
    #     validator = CursoValidator()
    #     current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Sep 1 2011', '%b %d %Y'))
    #
    #     #type(settings_mock).MIN_YEAR = PropertyMock(return_value=2011)
    #     #settings_mock.configure_mock(MIN_YEAR=2011)
    #     #settings_mock.YEARS_IN_ADVANCE = 1
    #     #settings_mock.CURSO_CHANGE_MONTH = 10
    #
    #     self.assertRaises(ValidationError, validator.__call__,(2010))
    #
    #     current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Aug 1 2011', '%b %d %Y'))
    #     self.assertEqual(None, validator.__call__(2011))
    #
    #     self.assertRaises(ValidationError, validator.__call__, (2013))
    #
    # @patch('tasas.models.datetime')
    # def test_curso_choices(self, current_curso_mock):
    #     current_curso_mock.date.today = Mock(return_value=datetime.datetime.strptime('Sep 1 2011', '%b %d %Y'))
    #     self.assertEqual(((2011, '2011/2012'), (2012, '2012/2013')), curso_choices())


class TestTasaModel(TestCase):
    curso = Curso()
    curso.anno = 2011

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
        tasa.curso = self.curso

        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas1 = 10
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas2 = 20
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas3 = 30
        self.assertRaises(ValidationError, tasa.clean)
        tasa.tasas4 = 40
        self.assertEqual(None, tasa.clean())

    def test_validator_precio_por_credito_2(self):
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
        tasa.curso = self.curso

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
        tasa.curso = self.curso

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
        tasa.curso = self.curso

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

from django.template import Context, Template, TemplateSyntaxError


class TestIncrementTemplate(TestCase):

    def test_increment_valid(self):
        context = Context({'12aa': '12aa'})
        self.assertEqual('2', Template('{% load increment %}' '{% increment 1%}').render(context))
        self.assertRaises(TemplateSyntaxError, Template, '{% load increment %}' '{% increment 1 2 3%}')
        self.assertRaises(TemplateSyntaxError, Template, '{% load increment %}' '{% increment '' %}')
        self.assertRaises(TemplateSyntaxError, Template('{% load increment %}' '{% increment 12aa %}').render, context)


class TestUniversidadForm(TestCase):
    # The form is almost entirely managed by Django, so this test makes little sense
    def test_valid_data(self):
        form = UniversidadForm({})

        self.assertFalse(form.is_valid())
        # self.assertEqual(form.errors, {})

