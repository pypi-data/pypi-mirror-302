import subprocess

class ManejadorRutasBandas:
    def __init__(self, carpeta_recortadas):
        self.carpeta_recortadas = carpeta_recortadas.replace(" ", "\ ")
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
        return self.rutas.get(banda)

    def establecer_ruta(self, banda, ruta):
        self.rutas[banda] = ruta