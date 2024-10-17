"""
Módulo: calculador_campo_atraccion

Este módulo contiene la clase `CalculadorCampoAtraccion`, que se utiliza para calcular el campo
de atracción basado en la urbanización.

Clases:
    - CalculadorCampoAtraccion: Hereda de `CalculadorMapaBase` y calcula el campo de atracción
                                para una matriz de urbanización dada.

Funciones:
    - calcular_mapa: Calcula el mapa del campo de atracción para la urbanización especificada.
"""

import numpy as np

from modulos.calculador.calculador_mapa_base import CalculadorMapaBase
from modulos.calculo_de_atraccion import calculo_campo_atraccion

class CalculadorCampoAtraccion(CalculadorMapaBase):
    """Clase que permite el cálculo del campo de atracción a partir de


    Args:
        CalculadorMapaBase (CalculadorMapaBase): Clase de la cual hereda
    """
    def __init__(self, carpeta_recortadas, urbanizacion : np.ndarray):
        """
        Inicializa la clase CalculadorCampoAtraccion.

        Args:
            carpeta_recortadas (str): Ruta a la carpeta de imágenes recortadas.
            urbanizacion (np.ndarray): Matriz de urbanización.
        """
        super().__init__(carpeta_recortadas)
        self.urbanizacion = urbanizacion

    def calcular_mapa(self):
        """
        Calcula el mapa del campo de atracción para la urbanización especificada.

        Returns:
            Resultado del cálculo del campo de atracción.
        """
        return calculo_campo_atraccion(self.urbanizacion)
    