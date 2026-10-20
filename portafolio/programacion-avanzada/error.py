"""Excepciones canónicas de la rúbrica y aliases de la descripción histórica."""


class Error(Exception):
    """Base de los errores de negocio de campañas y anuncios."""


class LargoExcedidoError(Error):
    """El nombre de campaña excede los 200 caracteres permitidos."""


class SubTipoInvalidoError(Error):
    """El subtipo no pertenece a los permitidos por el formato del anuncio."""


# Compatibilidad de imports; las clases y errores lanzados son los de la rúbrica.
LargoExcedidoException = LargoExcedidoError
SubTipoInvalidoException = SubTipoInvalidoError
