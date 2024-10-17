"""
Módulo: clasificador_urbanizacion

Este módulo contiene la clase `ClasificadorUrbanizacion`, que se utiliza para clasificar áreas de
urbanización en imágenes recortadas utilizando índices espectrales.

Clases:
    - ClasificadorUrbanizacion: Hereda de `ClasificadorBase` y clasifica áreas de urbanización en
                                imágenes recortadas.

Métodos:
    - clasificar: Clasifica áreas de urbanización en imágenes recortadas utilizando índices
                    espectrales.
"""

from modulos.clasificadores import clasificar_urbanizacion
from modulos.clasificador.clasificador_base import ClasificadorBase

class ClasificadorUrbanizacion(ClasificadorBase):
    """
    Clase para clasificar áreas de urbanización en imágenes recortadas utilizando índices
    espectrales.

    Hereda de:
        ClasificadorBase

    Métodos:
        - clasificar: Clasifica áreas de urbanización en imágenes recortadas utilizando índices
                        espectrales.
    """

    def clasificar(self):
        """
        Clasifica áreas de urbanización en imágenes recortadas utilizando índices espectrales.

        Utiliza los índices espectrales NDBI, NDBAI, NDMI y NDVI para realizar la clasificación.

        Returns:
            np.ndarray: Resultado de la clasificación de urbanización.
        """
        return clasificar_urbanizacion(self.rutas_indices['NDBI'],
                                       self.rutas_indices['NDBAI'],
                                       self.rutas_indices['NDMI'],
                                       self.rutas_indices['NDVI'])
