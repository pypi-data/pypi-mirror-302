"""
Módulo: manejador_rutas_bandas

Este módulo contiene la clase `ManejadorRutasBandas`, que se utiliza para gestionar las rutas de
las bandas espectrales en una carpeta de imágenes recortadas.

Clases:
    - ManejadorRutasBandas: Gestiona las rutas de las bandas espectrales en una carpeta de
                            imágenes recortadas.

Métodos:
    - __init__: Inicializa la clase con la carpeta de imágenes recortadas y configura las rutas de
                las bandas.
    - cargar_rutas: Carga las rutas de las bandas espectrales desde la carpeta de imágenes
                    recortadas.
    - obtener_ruta: Obtiene la ruta de una banda específica.
    - establecer_ruta: Establece la ruta de una banda específica.
"""
import subprocess

class ManejadorRutasBandas:
    """
    Clase para gestionar las rutas de las bandas espectrales en una carpeta de imágenes recortadas.

    Atributos:
        carpeta_recortadas (str): Ruta a la carpeta de imágenes recortadas.
        rutas (dict): Diccionario con las rutas de las bandas espectrales.
    """

    def __init__(self, carpeta_recortadas):
        """
        Inicializa la clase ManejadorRutasBandas.

        Args:
            carpeta_recortadas (str): Ruta a la carpeta de imágenes recortadas.
        """
        self.carpeta_recortadas = carpeta_recortadas.replace(" ", r"\ ")
        self.rutas = {
            'B4': None,
            'B5': None,
            'B3': None,
            'B6': None,
            'B10': None,
            'NDVI': f"{self.carpeta_recortadas}/ndvi.TIF",
            'NDWI': f"{self.carpeta_recortadas}/ndwi.TIF",
            'NDBI': f"{self.carpeta_recortadas}/ndbi.TIF",
            'NDBAI': f"{self.carpeta_recortadas}/ndbai.TIF",
            'NDMI': f"{self.carpeta_recortadas}/ndmi.TIF"
        }
        self.cargar_rutas()

    def cargar_rutas(self):
        """
        Carga las rutas de las bandas espectrales desde la carpeta de imágenes recortadas.

        Utiliza el comando `ls` para buscar archivos de bandas espectrales en la carpeta de
        imágenes recortadas y actualiza el diccionario de rutas.

        Returns:
            None
        """
        bandas = ["B4", "B5", "B3", "B6", "B10"]
        for banda in bandas:
            ruta = subprocess.run(f"ls {self.carpeta_recortadas}/*{banda}.TIF",
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  check=False).stdout.strip("\n")
            self.rutas[banda] = ruta

    def obtener_ruta(self, banda):
        """
        Obtiene la ruta de una banda específica.

        Args:
            banda (str): Nombre de la banda espectral.

        Returns:
            str: Ruta de la banda espectral.
        """
        return self.rutas.get(banda)

    def establecer_ruta(self, banda, ruta):
        """
        Establece la ruta de una banda específica.

        Args:
            banda (str): Nombre de la banda espectral.
            ruta (str): Ruta de la banda espectral.

        Returns:
            None
        """
        self.rutas[banda] = ruta
