"""
Módulo: calculador_indices

Este módulo contiene la clase `CalculadorIndices`, que se utiliza para calcular varios índices
espectrales (NDVI, NDWI, NDBI, NDBAI, NDMI) utilizando las rutas de las bandas espectrales
proporcionadas por un manejador de rutas.

Clases:
    - CalculadorIndices: Calcula índices espectrales utilizando las rutas de las bandas espectrales.

Métodos:
    - __init__: Inicializa la clase con un manejador de rutas.
    - calcular_indices: Calcula los índices espectrales NDVI, NDWI, NDBI, NDBAI y NDMI.
"""
from modulos.calculo_indices import calcular_ndvi, calcular_ndwi, calcular_ndbi, calcular_ndbai

class CalculadorIndices:
    """
    Clase para calcular varios índices espectrales utilizando las rutas de las bandas espectrales.

    Atributos:
        manejador_rutas (ManejadorRutasBandas): Manejador de rutas de las bandas espectrales.
    """

    def __init__(self, manejador_rutas):
        """
        Inicializa la clase CalculadorIndices.

        Args:
            manejador_rutas (ManejadorRutasBandas): Manejador de rutas de las bandas espectrales.
        """
        self.manejador_rutas = manejador_rutas

    def calcular_indices(self):
        """
         Calcula los índices espectrales NDVI, NDWI, NDBI, NDBAI y NDMI.

         Utiliza las rutas de las bandas espectrales proporcionadas por el manejador de rutas
         para calcular los índices y guarda los resultados en las rutas especificadas.

         Returns:
             None
         """
        calcular_ndvi(self.manejador_rutas.obtener_ruta('B4'),
                      self.manejador_rutas.obtener_ruta('B5'),
                      self.manejador_rutas.obtener_ruta('NDVI'))
        print("\t- Se calculó el NDVI")

        calcular_ndwi(self.manejador_rutas.obtener_ruta('B3'),
                      self.manejador_rutas.obtener_ruta('B5'),
                      self.manejador_rutas.obtener_ruta('NDWI'))
        print("\t- Se calculó el NDWI")

        calcular_ndbi(self.manejador_rutas.obtener_ruta('B5'),
                      self.manejador_rutas.obtener_ruta('B6'),
                      self.manejador_rutas.obtener_ruta('NDBI'))
        print("\t- Se calculó el NDBI")

        calcular_ndbai(self.manejador_rutas.obtener_ruta('B6'),
                       self.manejador_rutas.obtener_ruta('B10'),
                       self.manejador_rutas.obtener_ruta('NDBAI'))
        print("\t- Se calculó el NDBaI")

        calcular_ndbi(self.manejador_rutas.obtener_ruta('B5'),
                      self.manejador_rutas.obtener_ruta('B6'),
                      self.manejador_rutas.obtener_ruta('NDMI'))
        print("\t- Se calculó el NDMI")
        