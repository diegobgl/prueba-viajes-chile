from datetime import date
from pathlib import Path
from anuncio import Anuncio
from campaña import Campaña
from error import Error


def main(input_fn=None, log_path=None):
    input_fn = input if input_fn is None else input_fn
    log_path = Path(__file__).with_name('error.log') if log_path is None else Path(log_path)
    campaña = Campaña('Campaña de demostración', date(2026, 10, 1), date(2026, 10, 31), [
        {'formato': 'Video', 'url_archivo': 'video-demo.mp4', 'url_clic': 'https://example.com', 'duracion': 30, 'sub_tipo': 'instream'},
    ])
    try:
        campaña.nombre = input_fn('Nuevo nombre: ')
        campaña.anuncios[0].sub_tipo = input_fn('Nuevo subtipo de Video (instream/outstream): ')
    except (Error, TypeError, ValueError) as exception:
        with log_path.open('a', encoding='utf-8') as log:
            log.write(f'{type(exception).__name__}: {exception}\n')
        print(f'Error registrado: {exception}')
    print(campaña)
    Anuncio.mostrar_formatos()
    return campaña


if __name__ == '__main__':
    main()
