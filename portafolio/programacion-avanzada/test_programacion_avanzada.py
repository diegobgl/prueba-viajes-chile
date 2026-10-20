import contextlib
from datetime import date, datetime
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from anuncio import Anuncio, Video, Display, Social
from campaña import Campaña
from demo import main
from error import Error, LargoExcedidoError, SubTipoInvalidoError, LargoExcedidoException, SubTipoInvalidoException


VIDEO = {'formato': 'Video', 'url_archivo': 'video.mp4', 'url_clic': 'https://example.com', 'duracion': 30, 'sub_tipo': 'instream'}
DISPLAY = {'formato': 'Display', 'ancho': 300, 'alto': 250, 'url_archivo': 'banner.png', 'url_clic': 'https://example.com', 'sub_tipo': 'native'}
SOCIAL = {'formato': 'Social', 'ancho': 640, 'alto': 480, 'url_archivo': 'social.png', 'url_clic': 'https://example.com', 'sub_tipo': 'facebook'}


class CampañaTests(unittest.TestCase):
    def campaña(self, anuncios=None, nombre='Campaña de prueba'):
        return Campaña(nombre, date(2026, 10, 1), date(2026, 10, 31), [dict(VIDEO)] if anuncios is None else anuncios)

    def test_nombre_200_aceptado_201_rechazado_y_asignacion_fallida_conserva_nombre(self):
        campaña = self.campaña(nombre='a' * 200)
        self.assertEqual(campaña.nombre, 'a' * 200)
        campaña.nombre = 'ñ' * 200
        with self.assertRaises(LargoExcedidoError):
            campaña.nombre = 'ñ' * 201
        self.assertEqual(campaña.nombre, 'ñ' * 200)
        with self.assertRaises(LargoExcedidoError):
            self.campaña(nombre='x' * 201)

    def test_excepciones_canonicas_y_aliases_compatibles(self):
        self.assertTrue(issubclass(LargoExcedidoError, Error))
        self.assertTrue(issubclass(SubTipoInvalidoError, Error))
        self.assertTrue(issubclass(Error, Exception))
        self.assertIs(LargoExcedidoException, LargoExcedidoError)
        self.assertIs(SubTipoInvalidoException, SubTipoInvalidoError)
        self.assertEqual(LargoExcedidoError.__name__, 'LargoExcedidoError')
        self.assertEqual(SubTipoInvalidoError.__name__, 'SubTipoInvalidoError')

    def test_fechas_tienen_getters_setters_privados_y_str_muestra_ambas(self):
        campaña = self.campaña([dict(VIDEO), dict(DISPLAY), dict(DISPLAY), dict(SOCIAL)])
        campaña.fecha_inicio = date(2026, 11, 3)
        campaña.fecha_termino = date(2026, 12, 5)
        self.assertEqual(campaña.fecha_inicio, date(2026, 11, 3))
        self.assertEqual(campaña.fecha_termino, date(2026, 12, 5))
        texto = str(campaña)
        for expected in ('Campaña de prueba', '2026-11-03', '2026-12-05', '1 Video, 2 Display, 1 Social'):
            self.assertIn(expected, texto)
        self.assertNotIn('fecha_inicio', campaña.__dict__)
        self.assertNotIn('fecha_termino', campaña.__dict__)
        self.assertIn('_Campaña__fecha_inicio', campaña.__dict__)

    def test_asignacion_de_fecha_no_agrega_regla_de_orden_no_solicitada(self):
        campaña = self.campaña()
        campaña.fecha_termino = date(2026, 9, 30)
        self.assertEqual(campaña.fecha_termino, date(2026, 9, 30))

    def test_nombre_y_fechas_rechazan_tipos_incorrectos_sin_cambiar_valores(self):
        campaña = self.campaña()
        for value in (None, 123, []):
            with self.subTest(value=value), self.assertRaises(TypeError):
                campaña.nombre = value
        for attr in ('fecha_inicio', 'fecha_termino'):
            anterior = getattr(campaña, attr)
            for value in ('2026-10-14', datetime(2026, 10, 14, 12), None, 10):
                with self.subTest(attr=attr, value=value), self.assertRaises(TypeError):
                    setattr(campaña, attr, value)
                self.assertEqual(getattr(campaña, attr), anterior)

    def test_constructor_y_setter_crean_componentes_sin_alias_de_datos(self):
        datos = [dict(VIDEO)]
        campaña = self.campaña(datos)
        otro = self.campaña(datos)
        self.assertIsNot(campaña.anuncios[0], otro.anuncios[0])
        datos[0]['duracion'] = 99
        self.assertEqual(campaña.anuncios[0].duracion, 30)
        datos_nuevos = [dict(DISPLAY), dict(SOCIAL)]
        campaña.anuncios = datos_nuevos
        datos_nuevos[0]['ancho'] = 999
        self.assertEqual(campaña.anuncios[0].ancho, 300)
        self.assertIsInstance(campaña.anuncios[0], Display)
        self.assertIsInstance(campaña.anuncios[1], Social)

    def test_getter_devuelve_copia_y_setter_rechaza_instancias_externas(self):
        campaña = self.campaña()
        copia = campaña.anuncios
        copia.clear()
        self.assertEqual(len(campaña.anuncios), 1)
        externo = Video('externo.mp4', 'https://example.com', 15)
        with self.assertRaises(TypeError):
            campaña.anuncios = [externo]
        self.assertEqual(campaña.anuncios[0].duracion, 30)
        self.assertIsNot(campaña.anuncios[0], externo)

    def test_setter_anuncios_es_atomico_ante_error_en_ultimo_elemento(self):
        campaña = self.campaña()
        anterior = campaña.anuncios[0]
        with self.assertRaises(SubTipoInvalidoError):
            campaña.anuncios = [dict(DISPLAY), dict(SOCIAL, sub_tipo='inexistente')]
        self.assertEqual(len(campaña.anuncios), 1)
        self.assertIs(campaña.anuncios[0], anterior)
        for value, error in [(None, TypeError), ('Video', TypeError), ({'formato': 'Video'}, TypeError), ([], ValueError), ([{'formato': 'otro'}], ValueError)]:
            with self.subTest(value=value), self.assertRaises(error):
                campaña.anuncios = value
            self.assertIs(campaña.anuncios[0], anterior)

    def test_addAnuncio_crea_o_copia_y_no_adopta_instancia(self):
        campaña = self.campaña()
        externo = Display(120, 60, 'externo.png', 'https://example.com', 'traditional')
        campaña.addAnuncio(externo)
        self.assertIsNot(campaña.anuncios[1], externo)
        externo.ancho = 800
        self.assertEqual(campaña.anuncios[1].ancho, 120)
        campaña.addAnuncio(dict(SOCIAL))
        self.assertIsInstance(campaña.anuncios[2], Social)


class AnuncioTests(unittest.TestCase):
    def test_anuncio_es_abstracto_y_tres_formatos_heredan(self):
        with self.assertRaises(TypeError):
            Anuncio(1, 1, '', '')
        for clase in (Video, Display, Social):
            self.assertTrue(issubclass(clase, Anuncio))
        self.assertEqual(Video.SUB_TIPOS, ('instream', 'outstream'))
        self.assertEqual(Display.SUB_TIPOS, ('traditional', 'native'))
        self.assertEqual(Social.SUB_TIPOS, ('facebook', 'linkedin'))

    def test_dimensiones_no_positivas_se_vuelven_uno_y_setters_funcionan(self):
        for clase, subtipo in [(Display, 'traditional'), (Social, 'linkedin')]:
            anuncio = clase(0, -10, 'archivo.png', 'https://example.com', subtipo)
            self.assertEqual((anuncio.ancho, anuncio.alto), (1, 1))
            anuncio.ancho, anuncio.alto = 300, 250
            self.assertEqual((anuncio.ancho, anuncio.alto), (300, 250))
            for value in ('20', 20.5, True, None):
                with self.subTest(value=value), self.assertRaises(TypeError):
                    anuncio.ancho = value
            self.assertEqual(anuncio.ancho, 300)

    def test_video_uno_por_uno_inmutable_y_duracion_positiva_o_cinco(self):
        video = Video('video.mp4', 'https://example.com', 0)
        self.assertEqual((video.ancho, video.alto, video.duracion), (1, 1, 5))
        for value in (0, -50, 100, 'no se asigna'):
            video.ancho = value
            video.alto = value
            self.assertEqual((video.ancho, video.alto), (1, 1))
        video.duracion = -2
        self.assertEqual(video.duracion, 5)
        video.duracion = 45
        self.assertEqual(video.duracion, 45)
        for value in (True, '30', 1.5, None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                video.duracion = value
        self.assertEqual(video.duracion, 45)

    def test_url_getters_setters_basicos_y_subtipo_por_formato(self):
        anuncios = [Video('v.mp4', 'destino', 30), Display(1, 1, 'd.png', 'destino'), Social(1, 1, 's.png', 'destino')]
        for anuncio in anuncios:
            anuncio.url_archivo = 'nuevo archivo'
            anuncio.url_clic = ''
            self.assertEqual(anuncio.url_archivo, 'nuevo archivo')
            self.assertEqual(anuncio.url_clic, '')
            anuncio.sub_tipo = anuncio.SUB_TIPOS[-1]
            anterior = anuncio.sub_tipo
            with self.assertRaises(SubTipoInvalidoError):
                anuncio.sub_tipo = 'otro'
            self.assertEqual(anuncio.sub_tipo, anterior)
            with self.assertRaises(TypeError):
                anuncio.url_archivo = None

    def test_polimorfismo_y_colaboracion_muestran_mensajes_exactos(self):
        anuncios = [Video('v.mp4', '', 30), Display(1, 1, 'd.png', ''), Social(1, 1, 's.png', '')]
        expected = [
            'COMPRESIÓN DE VIDEO NO IMPLEMENTADA AÚN',
            'RECORTE DE VIDEO NO IMPLEMENTADO AÚN',
            'COMPRESIÓN DE ANUNCIOS DISPLAY NO IMPLEMENTADA AÚN',
            'REDIMENSIONAMIENTO DE ANUNCIOS DISPLAY NO IMPLEMENTADO AÚN',
            'COMPRESIÓN DE ANUNCIOS DE REDES SOCIALES NO IMPLEMENTADA AÚN',
            'REDIMENSIONAMIENTO DE ANUNCIOS DE REDES SOCIALES NO IMPLEMENTADO AÚN',
        ]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            for anuncio in anuncios:
                anuncio.comprimir_anuncio()
                anuncio.redimensionar_anuncio()
        self.assertEqual(output.getvalue().splitlines(), expected)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            Anuncio.mostrar_formatos()
        for palabra in ('Video', 'Display', 'Social', 'instream', 'outstream', 'traditional', 'native', 'facebook', 'linkedin'):
            self.assertIn(palabra, output.getvalue())


class DemoTests(unittest.TestCase):
    def run_demo(self, values, path):
        values = iter(values)
        with contextlib.redirect_stdout(io.StringIO()):
            return main(input_fn=lambda prompt: next(values), log_path=path)

    def test_demo_un_video_y_dos_inputs_validos_sin_crear_log(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as tmp:
            path = Path(tmp)/'error.log'
            campaña = self.run_demo(['Nombre válido', 'outstream'], path)
            self.assertEqual(campaña.nombre, 'Nombre válido')
            self.assertEqual(len(campaña.anuncios), 1)
            self.assertIsInstance(campaña.anuncios[0], Video)
            self.assertEqual(campaña.anuncios[0].sub_tipo, 'outstream')
            self.assertFalse(path.exists())

    def test_demo_append_utf8_registra_errores_200_y_subtipo(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as tmp:
            path = Path(tmp)/'error.log'
            path.write_text('línea anterior\n', encoding='utf-8')
            campaña = self.run_demo(['x' * 201], path)
            self.assertEqual(campaña.nombre, 'Campaña de demostración')
            campaña = self.run_demo(['Campaña corregida', 'subtipo inválido'], path)
            self.assertEqual(campaña.nombre, 'Campaña corregida')
            self.assertEqual(campaña.anuncios[0].sub_tipo, 'instream')
            text = path.read_text(encoding='utf-8')
            self.assertIn('línea anterior', text)
            self.assertIn('LargoExcedidoError: El nombre supera 200 caracteres.', text)
            self.assertIn('SubTipoInvalidoError: Subtipo inválido para Video', text)
            self.assertEqual(len(text.splitlines()), 3)

    def test_importar_demo_no_solicita_input(self):
        spec = importlib.util.spec_from_file_location('demo_importado_prueba', Path(__file__).with_name('demo.py'))
        module = importlib.util.module_from_spec(spec)
        with patch('builtins.input', side_effect=AssertionError('No debe ejecutar input al importar')):
            spec.loader.exec_module(module)
        self.assertTrue(callable(module.main))


if __name__ == '__main__':
    unittest.main()
