"""
Módulo: clasificador_suelos

Este módulo contiene la clase `ClasificadorSuelos`, que se utiliza para clasificar suelos
en imágenes recortadas utilizando índices espectrales.

Clases:
    - ClasificadorSuelos: Hereda de `ClasificadorBase` y clasifica suelos en imágenes recortadas.

Funciones:
    - clasificar: Clasifica suelos en imágenes recortadas utilizando índices espectrales
                    y muestra los resultados.
"""
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from modulos.clasificadores import clasificar_clases
from modulos.clasificador.clasificador_base import ClasificadorBase

class ClasificadorSuelos(ClasificadorBase):
    """
    Clase para clasificar suelos en imágenes recortadas utilizando índices espectrales.

    Hereda de:
        ClasificadorBase

    Atributos:
        carpeta_recortadas (str): Ruta a la carpeta de imágenes recortadas.
        rutas_indices (dict): Diccionario con las rutas a los archivos de índices espectrales.
    """
    def __init__(self, carpeta_recortadas, rutas_indices):
        """
        Inicializa la clase ClasificadorSuelos.

        Args:
            carpeta_recortadas (str): Ruta a la carpeta de imágenes recortadas.
            rutas_indices (dict): Diccionario con las rutas a los archivos de índices espectrales.
        """
        super().__init__(rutas_indices)
        self.carpeta_recortadas = carpeta_recortadas

    def clasificar(self):
        """
        Clasifica suelos en imágenes recortadas utilizando índices espectrales y muestra
        los resultados.

        Lee los índices espectrales desde las rutas especificadas, aplica la clasificación de
        suelos y muestra los resultados en un gráfico.

        Returns:
            None
        """
        archivo_clases = f"{self.carpeta_recortadas}/class.TIF"
        clasificar_clases(self.rutas_indices['NDVI'], self.rutas_indices['NDWI'], archivo_clases)

        with rasterio.open(archivo_clases) as src:
            clasificacion = src.read(1, masked=True)

        colors = ['brown', 'green', 'yellow', 'blue']
        cmap = ListedColormap(colors)
        _, ax = plt.subplots(figsize=(10, 10)) # pylint: disable=C0103
        im = ax.imshow(clasificacion, cmap=cmap, vmin=1, vmax=4, interpolation='none') # pylint: disable=C0103
        cbar = ax.figure.colorbar(im, ax=ax, ticks=[1, 2, 3, 4], orientation='vertical')
        cbar.ax.set_yticklabels(['Suelo expuesto', 'Vegetación baja', 'Vegetación alta', 'Agua'])
        cbar.set_label('Clases')
        ax.set_title('Clasificación de Imagen')
        plt.show()
        print("\nFinaliza clasificación de clases.")
