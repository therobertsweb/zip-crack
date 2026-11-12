# Probador de contrasenas ZIP

`crack_zip.py` prueba las contrasenas de una columna de un archivo CSV contra
un archivo ZIP cifrado local. No extrae el contenido del ZIP.

Usalo solo con archivos y listas de contrasenas que tengas autorizacion para
recuperar o administrar.

## Requisitos

- Python 3
- Un ZIP valido y cifrado con el formato compatible con la biblioteca estandar
  `zipfile` de Python
- Un CSV con encabezados y una columna de contrasenas

No requiere instalar paquetes adicionales.

## Uso

Desde esta carpeta:

```bash
python3 crack_zip.py archivo.zip contrasenas.csv
```

Por defecto, el script lee la columna `Password`:

```csv
Title,Password
Cuenta de ejemplo,mi-contrasena
```

Si la columna tiene otro nombre, indicalo con `--column`:

```bash
python3 crack_zip.py archivo.zip contrasenas.csv --column Clave
```

El script elimina intentos duplicados y omite valores vacios. Se detiene al
encontrar la primera contrasena valida.

## Resultado y codigos de salida

| Codigo | Significado |
| --- | --- |
| `0` | Se encontro una contrasena valida. |
| `1` | Ninguna contrasena del CSV fue valida. |
| `2` | Ocurrio un error, como un ZIP incompleto, una columna inexistente o un archivo inaccesible. |

## Problemas comunes

- **`File is not a zip file`**: el archivo esta dañado, incompleto o no es un
  ZIP valido. Descarga o copia el archivo nuevamente antes de ejecutar el
  script.
- **No se encontro la columna**: revisa los encabezados del CSV o usa
  `--column` con el nombre correcto.
- **El ZIP no contiene archivos cifrados**: el archivo no necesita
  contrasena.
# zip-crack
