from abc import ABC, abstractmethod
from error import SubTipoInvalidoError


def _entero(value, nombre):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f'{nombre} debe ser un entero.')
    return value


def _texto(value, nombre):
    if not isinstance(value, str):
        raise TypeError(f'{nombre} debe ser una cadena de texto.')
    return value


class Anuncio(ABC):
    def __init__(self, ancho, alto, url_archivo, url_clic, sub_tipo=None):
        self.ancho = ancho
        self.alto = alto
        self.url_archivo = url_archivo
        self.url_clic = url_clic
        self.sub_tipo = self.SUB_TIPOS[0] if sub_tipo is None else sub_tipo

    @property
    def ancho(self):
        return self.__ancho

    @ancho.setter
    def ancho(self, value):
        self.__ancho = max(1, _entero(value, 'Ancho'))

    @property
    def alto(self):
        return self.__alto

    @alto.setter
    def alto(self, value):
        self.__alto = max(1, _entero(value, 'Alto'))

    @property
    def url_archivo(self):
        return self.__url_archivo

    @url_archivo.setter
    def url_archivo(self, value):
        self.__url_archivo = _texto(value, 'URL del archivo')

    @property
    def url_clic(self):
        return self.__url_clic

    @url_clic.setter
    def url_clic(self, value):
        self.__url_clic = _texto(value, 'URL de clic')

    @property
    def sub_tipo(self):
        return self.__sub_tipo

    @sub_tipo.setter
    def sub_tipo(self, value):
        if value not in self.SUB_TIPOS:
            raise SubTipoInvalidoError(f'Subtipo inválido para {self.FORMATO}: {value}. Permitidos: {", ".join(self.SUB_TIPOS)}.')
        self.__sub_tipo = value

    @staticmethod
    def mostrar_formatos():
        for clase in (Video, Display, Social):
            print(f'{clase.FORMATO}:\n==========')
            for sub_tipo in clase.SUB_TIPOS:
                print(f'- {sub_tipo}')

    @abstractmethod
    def comprimir_anuncio(self):
        pass

    @abstractmethod
    def redimensionar_anuncio(self):
        pass


class Video(Anuncio):
    FORMATO = 'Video'
    SUB_TIPOS = ('instream', 'outstream')

    def __init__(self, url_archivo, url_clic, duracion, sub_tipo='instream'):
        super().__init__(1, 1, url_archivo, url_clic, sub_tipo)
        self.duracion = duracion

    @Anuncio.ancho.setter
    def ancho(self, value):
        # El formato Video conserva 1x1 incluso al intentar modificar dimensiones.
        self._Anuncio__ancho = 1

    @Anuncio.alto.setter
    def alto(self, value):
        self._Anuncio__alto = 1

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, value):
        value = _entero(value, 'Duración')
        self.__duracion = value if value > 0 else 5

    def comprimir_anuncio(self):
        print('COMPRESIÓN DE VIDEO NO IMPLEMENTADA AÚN')

    def redimensionar_anuncio(self):
        print('RECORTE DE VIDEO NO IMPLEMENTADO AÚN')


class Display(Anuncio):
    FORMATO = 'Display'
    SUB_TIPOS = ('traditional', 'native')

    def comprimir_anuncio(self):
        print('COMPRESIÓN DE ANUNCIOS DISPLAY NO IMPLEMENTADA AÚN')

    def redimensionar_anuncio(self):
        print('REDIMENSIONAMIENTO DE ANUNCIOS DISPLAY NO IMPLEMENTADO AÚN')


class Social(Anuncio):
    FORMATO = 'Social'
    SUB_TIPOS = ('facebook', 'linkedin')

    def comprimir_anuncio(self):
        print('COMPRESIÓN DE ANUNCIOS DE REDES SOCIALES NO IMPLEMENTADA AÚN')

    def redimensionar_anuncio(self):
        print('REDIMENSIONAMIENTO DE ANUNCIOS DE REDES SOCIALES NO IMPLEMENTADO AÚN')
