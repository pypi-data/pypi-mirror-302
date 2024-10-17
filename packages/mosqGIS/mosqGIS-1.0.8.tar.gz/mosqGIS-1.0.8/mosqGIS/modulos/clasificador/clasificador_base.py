"""
Módulo: clasificador_base

Este módulo contiene la clase `ClasificadorBase`, que sirve como clase base para los
clasificadores de imágenes utilizando índices espectrales.

Clases:
    - ClasificadorBase: Clase base para clasificadores de imágenes.

Métodos:
    - __init__: Inicializa la clase con las rutas de los índices espectrales.
    - clasificar: Método abstracto que debe ser implementado por las subclases.
"""
class ClasificadorBase:
    """
    Clase base para clasificadores de imágenes utilizando índices espectrales.

    Atributos:
        rutas_indices (dict): Diccionario con las rutas a los archivos de índices espectrales.
    """

    def __init__(self, rutas_indices):
        """
        Inicializa la clase ClasificadorBase.

        Args:
            rutas_indices (dict): Diccionario con las rutas a los archivos de índices espectrales.
        """
        self.rutas_indices = rutas_indices

    def clasificar(self):
        """
        Método abstracto que debe ser implementado por las subclases.

        Raises:
            NotImplementedError: Si la subclase no implementa este método.
        """
        raise NotImplementedError("Subclasses should implement this method")
