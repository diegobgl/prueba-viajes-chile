# Programación Avanzada — prueba académica principal

Prueba 792246 del curso Full Stack Python SENCE. Esta copia conserva el código de la versión corregida 16 y es el trabajo evaluado principal del portafolio.

## Problema y solución

Representar una campaña con anuncios de distintos formatos. `Anuncio` define el contrato abstracto; Video, Display y Social especializan sus propiedades y comportamiento. `Campaña` crea sus componentes desde datos, valida cambios y mantiene una representación con nombre, fechas y cantidades.

Las correcciones cubren límite de nombre de 200 caracteres, tipos y subtipos, excepciones específicas, fechas, dimensiones de Video, composición sin compartir componentes externos, aislamiento de la lista expuesta y reemplazo atómico. `demo.py` realiza dos asignaciones dentro de try/except y agrega los errores a `error.log` en UTF-8, conservando el registro anterior.

## Ejecutar

Python 3.12 o superior, biblioteca estándar y sin dependencias externas:

```powershell
python demo.py
python -m unittest discover -v
```

La demo crea exactamente un Video y solicita nombre y subtipo. Usar instream/outstream para el caso válido; un nombre demasiado largo o un subtipo de otro formato permite comprobar el manejo de errores. Importar `demo` no solicita datos ni ejecuta la demostración.

## Evidencia

[VALIDACION.txt](VALIDACION.txt) registra 17 tests aprobados al verificar esta copia pública el 20/10/2026. [EVIDENCIA_DEMO.txt](EVIDENCIA_DEMO.txt) conserva tres ejecuciones reales de consola con datos ficticios: caso válido, nombre excesivo y subtipo inválido. Los tests verifican límites, errores compatibles, fechas, abstracción, herencia, colaboración, composición, aislamiento, atomicidad y registro acumulativo UTF-8.

Los métodos de compresión/redimensionamiento muestran mensajes didácticos; no implementan procesamiento multimedia. No se declara una aplicación desplegada ni experiencia empresarial.

Esta copia contiene código y registros técnicos saneados. Se dejó fuera el diagrama docente de apoyo; permanece en la entrega LMS 16 y no se asume licencia para publicarlo. Tampoco se copió el documento de feedback íntegro ni notas personales. El código procede de un ejercicio académico del curso y conserva ese contexto.
