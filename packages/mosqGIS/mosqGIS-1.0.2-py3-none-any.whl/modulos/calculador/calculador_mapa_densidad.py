"""
Este módulo contiene la clase `CalculadorMapaDensidad`, que se utiliza para calcular mapas de densidad utilizando imágenes de fondo y datos de ovitrampas.

Clases:
    CalculadorMapaDensidad: Una clase para calcular mapas de densidad.
"""

from mosqGIS.modulos.calculador.calculador_mapa_base import CalculadorMapaBase
from mosqGIS.modulos import obtener_densidad_inicial

class CalculadorMapaDensidad(CalculadorMapaBase):
    def __init__(self, carpeta_recortadas, ruta_datos_ovitrampas):
        """
        Inicializa la clase `CalculadorMapaDensidad`.

        Args:
            carpeta_recortadas (str): Ruta a la carpeta que contiene las imágenes recortadas.
            ruta_datos_ovitrampas (str): Ruta al archivo que contiene los datos de ovitrampas.
        """
        super().__init__(carpeta_recortadas)
        self.ruta_datos_ovitrampas = ruta_datos_ovitrampas

    def calcular_mapa(self, imagen_fondo):
        """
        Calcula el mapa de densidad utilizando la imagen de fondo y los datos de ovitrampas.

        Args:
            imagen_fondo (str): Ruta a la imagen de fondo.

        Returns:
            object: El resultado del cálculo de densidad.
        """
        return obtener_densidad_inicial(imagen_fondo, self.ruta_datos_ovitrampas)