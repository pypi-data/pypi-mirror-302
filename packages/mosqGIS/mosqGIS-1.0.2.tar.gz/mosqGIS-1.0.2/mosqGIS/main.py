"""
main.py

Este módulo es el punto de entrada para procesar carpetas de imágenes y rutas de {
polígonos utilizando varias funciones de procesamiento de imágenes y análisis geoespacial.

Dependencias:
-------------
- os: Proporciona una forma de usar funcionalidades dependientes del sistema operativo.
- subprocess: Permite la ejecución de comandos del sistema.
- argparse: Facilita la escritura de interfaces de línea de comandos amigables.
- rasterio: Biblioteca para leer y escribir datos raster.
- matplotlib: Biblioteca para la generación de gráficos en Python.
- modulos.cropTIF: Módulo para recortar imágenes TIF.
- modulos.calculo_indices: Módulo para calcular índices como NDVI, NDWI, NDBI y NDBAI.
- modulos.clasificador: Módulo para clasificar imágenes en diferentes clases y urbanización.
- modulos.calculo_de_atracción: Módulo para calcular el campo de atracción basado 
                                en la proximidad de viviendas.
- modulos.obtener_densidad_inicial: Módulo para obtener la densidad inicial de una región.

Argumentos:
-----------
- --carpeta_recortadas: Carpeta para imágenes recortadas.
- --carpeta_no_recortadas: Carpeta para imágenes no recortadas.
- --ruta_poligono: Ruta del archivo de polígono.
- --ruta_datos_ovitrampas: Ruta del archivo de datos de ovitrampas.

Ejemplo de uso:
---------------
python main.py  --carpeta_recortadas /ruta/a/carpeta_recortadas 
                --carpeta_no_recortadas /ruta/a/carpeta_no_recortadas 
                --ruta_poligono /ruta/a/poligono 
                --ruta_datos_ovitrampas /ruta/a/datos_ovitrampas
"""

import os
from modulos.clasificador.clasificador_urbanizacion import ClasificadorUrbanizacion
from modulos.manejador.manejador_argumentos import ManejadorArgumentos
from modulos.procesador.procesador_imagenes import RecortadorImagenes
from modulos.calculador.calculador_indices import CalculadorIndices
from modulos.clasificador.clasificador_suelos import ClasificadorSuelos
from modulos.calculador.calculador_campo_atraccion import CalculadorCampoAtraccion
from modulos.calculador.calculador_mapa_densidad import CalculadorMapaDensidad
from modulos.manejador.manejador_rutas_bandas import ManejadorRutasBandas

def main():
    arg_handler = ManejadorArgumentos()
    args = arg_handler.obtener_argumentos()

    carpeta_recortadas = args.carpeta_recortadas or input("Por favor, ingrese la carpeta para imágenes recortadas: ")
    carpeta_no_recortadas = args.carpeta_no_recortadas or input("Por favor, ingrese la carpeta para imágenes no recortadas: ")
    ruta_poligono = os.path.abspath(args.ruta_poligono or input("Por favor, ingrese la ruta del archivo de polígono: "))
    ruta_datos_ovitrampas = os.path.abspath(args.ruta_datos_ovitrampas or input("Por favor, ingrese la ruta del archivo de datos de ovitrampas: "))

    carpeta_recortadas = os.path.abspath(carpeta_recortadas)
    #carpeta_recortadas = carpeta_recortadas.replace(" ", "\ ")
    carpeta_no_recortadas = os.path.abspath(carpeta_no_recortadas)
    #carpeta_no_recortadas = carpeta_no_recortadas.replace(" ", "\ ")

    manejador_rutas_bandas = ManejadorRutasBandas(carpeta_recortadas)

    recortador_imagenes = RecortadorImagenes(carpeta_recortadas, carpeta_no_recortadas, ruta_poligono)
    recortador_imagenes.recortar_imagenes()

    calculador_indices = CalculadorIndices(manejador_rutas_bandas)
    calculador_indices.calcular_indices()

    rutas_indices = {
        'NDVI': manejador_rutas_bandas.obtener_ruta('NDVI'),
        'NDWI': manejador_rutas_bandas.obtener_ruta('NDWI'),
        'NDBI': manejador_rutas_bandas.obtener_ruta('NDBI'),
        'NDBAI': manejador_rutas_bandas.obtener_ruta('NDBAI'),
        'NDMI': manejador_rutas_bandas.obtener_ruta('NDMI')
    }

    clasificador_suelos = ClasificadorSuelos(carpeta_recortadas, rutas_indices)
    clasificador_suelos.clasificar()

    clasificador_urbanizacion = ClasificadorUrbanizacion(rutas_indices)
    urbanizacion = clasificador_urbanizacion.clasificar()

    calculador_campo_atraccion = CalculadorCampoAtraccion(carpeta_recortadas, urbanizacion)
    calculador_campo_atraccion.calcular_mapa()

    calculador_mapa_densidad = CalculadorMapaDensidad(carpeta_recortadas, ruta_datos_ovitrampas)
    calculador_mapa_densidad.calcular_mapa(manejador_rutas_bandas.obtener_ruta('B4'))

if __name__ == "__main__":
    main()
