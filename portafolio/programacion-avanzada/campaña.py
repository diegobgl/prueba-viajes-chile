from collections.abc import Mapping
from datetime import date, datetime
from anuncio import Anuncio, Video, Display, Social
from error import LargoExcedidoError


class Campaña:
    MAX_NOMBRE = 200

    def __init__(self, nombre, fecha_inicio, fecha_termino, anuncios):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_termino = fecha_termino
        self.anuncios = anuncios

    @staticmethod
    def __crear_anuncio(datos):
        if not isinstance(datos, Mapping):
            raise TypeError('Cada anuncio debe describirse mediante un diccionario de datos.')
        atributos = dict(datos)
        formato = atributos.pop('formato', None)
        clases = {'Video': Video, 'Display': Display, 'Social': Social}
        if formato not in clases:
            raise ValueError(f'Formato de anuncio inválido: {formato}.')
        return clases[formato](**atributos)

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        if not isinstance(value, str):
            raise TypeError('El nombre debe ser una cadena de texto.')
        if len(value) > self.MAX_NOMBRE:
            raise LargoExcedidoError(f'El nombre supera {self.MAX_NOMBRE} caracteres.')
        self.__nombre = value

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, value):
        if not isinstance(value, date) or isinstance(value, datetime):
            raise TypeError('fecha_inicio debe ser datetime.date.')
        self.__fecha_inicio = value

    @property
    def fecha_termino(self):
        return self.__fecha_termino

    @fecha_termino.setter
    def fecha_termino(self, value):
        if not isinstance(value, date) or isinstance(value, datetime):
            raise TypeError('fecha_termino debe ser datetime.date.')
        self.__fecha_termino = value

    @property
    def anuncios(self):
        return self.__anuncios.copy()

    @anuncios.setter
    def anuncios(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError('anuncios debe ser una lista o tupla de diccionarios.')
        if not value:
            raise ValueError('La campaña debe contener al menos un anuncio, según el diagrama 1..*.')
        # Crear todos antes de asignar: un dato inválido no reemplaza parcialmente la lista.
        nuevos = [self.__crear_anuncio(datos) for datos in value]
        self.__anuncios = nuevos

    def addAnuncio(self, anuncio):
        """Crea un componente; una instancia recibida se copia, nunca se adopta."""
        if isinstance(anuncio, Anuncio):
            datos = {'formato': anuncio.FORMATO, 'url_archivo': anuncio.url_archivo, 'url_clic': anuncio.url_clic, 'sub_tipo': anuncio.sub_tipo}
            if isinstance(anuncio, Video):
                datos['duracion'] = anuncio.duracion
            else:
                datos.update(ancho=anuncio.ancho, alto=anuncio.alto)
        else:
            datos = anuncio
        nuevo = self.__crear_anuncio(datos)
        self.__anuncios.append(nuevo)

    def __str__(self):
        counts = {clase.FORMATO: sum(isinstance(anuncio, clase) for anuncio in self.__anuncios) for clase in (Video, Display, Social)}
        return (f'Nombre de la campaña: {self.nombre}\n'
                f'Fecha inicio: {self.fecha_inicio.isoformat()}\n'
                f'Fecha término: {self.fecha_termino.isoformat()}\n'
                f'Anuncios: {counts["Video"]} Video, {counts["Display"]} Display, {counts["Social"]} Social')
