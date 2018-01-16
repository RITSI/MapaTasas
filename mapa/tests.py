from django.test import TestCase
# from django.core.validators import ValidationError
# from mock import patch, Mock
# from datetime import datetime
# from .models import Reporte

# Create your tests here.
class TestReporteModel(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

# TODO: Volver a utilizar el test el día que esté implementado el validador que comprueba el curso.
#    @patch('tasas.models.datetime')
#     def test_invalid_curso(self, current_curso_mock):
#         current_curso_mock.date.today = Mock(return_value=datetime.strptime('Sep 1 2011', '%b %d %Y'))
#         reporte = Reporte()
#
#         reporte.descripcion = "Bla"
#         reporte.curso = 2010
#
#         self.assertRaises(ValidationError, reporte.clean_fields)
#
#         current_curso_mock.date.today = Mock(return_value=datetime.today())
#
#         reporte.curso = datetime.today().year
#         self.assertEqual(None, reporte.clean_fields())
