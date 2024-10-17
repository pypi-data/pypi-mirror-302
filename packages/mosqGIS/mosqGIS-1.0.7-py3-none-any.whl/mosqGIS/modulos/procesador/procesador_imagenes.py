"""
Módulo: procesador_imagenes

Este módulo contiene la clase `RecortadorImagenes`, que se utiliza para recortar imágenes basadas
en un polígono dado.

Clases:
    - RecortadorImagenes: Recorta imágenes en una carpeta especificada basándose en un polígono
                            dado.
"""
import os
from modulos.crop_tif import crop_tif

class RecortadorImagenes:
    """
    Clase para recortar imágenes basadas en un polígono dado.

    Atributos:
        carpeta_recortadas (str): Ruta a la carpeta de imágenes recortadas.
        carpeta_no_recortadas (str): Ruta a la carpeta de imágenes no recortadas.
        ruta_poligono (str): Ruta al archivo del polígono utilizado para recortar.
    """

    def __init__(self, carpeta_recortadas, carpeta_no_recortadas, ruta_poligono):
        """
        Inicializa la clase RecortadorImagenes.

        Args:
            carpeta_recortadas (str): Ruta a la carpeta de imágenes recortadas.
            carpeta_no_recortadas (str): Ruta a la carpeta de imágenes no recortadas.
            ruta_poligono (str): Ruta al archivo del polígono utilizado para recortar.
        """
        self.carpeta_recortadas = carpeta_recortadas
        self.carpeta_no_recortadas = carpeta_no_recortadas
        self.ruta_poligono = ruta_poligono

    def recortar_imagenes(self):
        """
        Recorta imágenes en la carpeta especificada y guarda los resultados en otra carpeta.

        Verifica si la carpeta de imágenes recortadas existe, y si no, la crea. Luego, itera
        sobre las imágenes no recortadas, las recorta utilizando el polígono especificado y guarda
        los resultados en la carpeta de imágenes recortadas.

        Returns:
            None
        """
        if os.path.exists(self.carpeta_recortadas):
            print(f"La carpeta '{self.carpeta_recortadas}' existe.")
            os.system(f"rm -rf {self.carpeta_recortadas}/*")
        else:
            print(f"La carpeta '{self.carpeta_recortadas}' no existe. Se creará ahora.")
            try:
                os.makedirs(self.carpeta_recortadas)
                print(f"Se ha creado la carpeta '{self.carpeta_recortadas}/'.")
            except OSError as error:
                print(f"No se pudo crear la carpeta '{self.carpeta_recortadas}': {error}")

        for nombre_archivo in os.listdir(self.carpeta_no_recortadas):
            if nombre_archivo.endswith(".TIF") or nombre_archivo.endswith(".tif"):
                ruta_completa = os.path.join(self.carpeta_no_recortadas, nombre_archivo)
                crop_tif(ruta_completa,
                         f"{self.carpeta_recortadas}/{nombre_archivo}",
                         self.ruta_poligono)
