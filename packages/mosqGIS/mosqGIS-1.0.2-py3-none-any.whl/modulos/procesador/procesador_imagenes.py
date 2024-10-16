# procesador_imagenes.py
import os
from mosqGIS.modulos import crop_tif

class RecortadorImagenes:
    def __init__(self, carpeta_recortadas, carpeta_no_recortadas, ruta_poligono):
        self.carpeta_recortadas = carpeta_recortadas
        self.carpeta_no_recortadas = carpeta_no_recortadas
        self.ruta_poligono = ruta_poligono

    def recortar_imagenes(self):
        if os.path.exists(self.carpeta_recortadas):
            print(f"La carpeta '{self.carpeta_recortadas}' existe.")
            os.system(f"rm -rf {self.carpeta_recortadas}/*")
        else:
            print(f"La carpeta '{self.carpeta_recortadas}' no existe. Se creará ahora.")
            try:
                os.makedirs(self.carpeta_recortadas)
                print(f"Se ha creado la carpeta '{self.carpeta_recortadas}/'.")
            except OSError as e:
                print(f"No se pudo crear la carpeta '{self.carpeta_recortadas}': {e}")

        for nombre_archivo in os.listdir(self.carpeta_no_recortadas):
            if nombre_archivo.endswith(".TIF") or nombre_archivo.endswith(".tif"):
                ruta_completa = os.path.join(self.carpeta_no_recortadas, nombre_archivo)
                crop_tif(ruta_completa, f"{self.carpeta_recortadas}/{nombre_archivo}", self.ruta_poligono)