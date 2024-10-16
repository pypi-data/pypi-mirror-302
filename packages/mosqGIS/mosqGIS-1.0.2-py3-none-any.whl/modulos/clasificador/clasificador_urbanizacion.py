# clasificador_urbanizacion.py
from mosqGIS.modulos.clasificadores import clasificar_urbanizacion
from mosqGIS.modulos import ClasificadorBase

class ClasificadorUrbanizacion(ClasificadorBase):
    def clasificar(self):
        return clasificar_urbanizacion(self.rutas_indices['NDBI'],
                                       self.rutas_indices['NDBAI'],
                                       self.rutas_indices['NDMI'],
                                       self.rutas_indices['NDVI'])