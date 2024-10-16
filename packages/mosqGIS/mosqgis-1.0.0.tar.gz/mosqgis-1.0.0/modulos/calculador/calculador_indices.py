from modulos.calculo_indices import calcular_ndvi, calcular_ndwi, calcular_ndbi, calcular_ndbai

class CalculadorIndices:
    def __init__(self, manejador_rutas):
        self.manejador_rutas = manejador_rutas

    def calcular_indices(self):
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