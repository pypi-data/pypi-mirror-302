# clasificador_suelos.py
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from modulos.clasificadores import clasificar_clases
from modulos.clasificador.clasificador_base import ClasificadorBase

class ClasificadorSuelos(ClasificadorBase):
    def __init__(self, carpeta_recortadas, rutas_indices):
        super().__init__(rutas_indices)
        self.carpeta_recortadas = carpeta_recortadas

    def clasificar(self):
        ARCHIVO_CLASES = f"{self.carpeta_recortadas}/class.TIF"
        clasificar_clases(self.rutas_indices['NDVI'], self.rutas_indices['NDWI'], ARCHIVO_CLASES)

        with rasterio.open(ARCHIVO_CLASES) as src:
            clasificacion = src.read(1, masked=True)
            profile = src.profile

        colors = ['brown', 'green', 'yellow', 'blue']
        cmap = ListedColormap(colors)
        fig, ax = plt.subplots(figsize=(10, 10))
        im = ax.imshow(clasificacion, cmap=cmap, vmin=1, vmax=4, interpolation='none')
        cbar = ax.figure.colorbar(im, ax=ax, ticks=[1, 2, 3, 4], orientation='vertical')
        cbar.ax.set_yticklabels(['Suelo expuesto', 'Vegetación baja', 'Vegetación alta', 'Agua'])
        cbar.set_label('Clases')
        ax.set_title('Clasificación de Imagen')
        plt.show()
        print("\nFinaliza clasificación de clases.")