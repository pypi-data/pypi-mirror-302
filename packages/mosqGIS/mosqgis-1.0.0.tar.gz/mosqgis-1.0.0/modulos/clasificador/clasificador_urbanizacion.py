# clasificador_urbanizacion.py
from modulos.clasificadores import clasificar_urbanizacion
from modulos.clasificador.clasificador_base import ClasificadorBase

class ClasificadorUrbanizacion(ClasificadorBase):
    def clasificar(self):
        return clasificar_urbanizacion(self.rutas_indices['NDBI'],
                                       self.rutas_indices['NDBAI'],
                                       self.rutas_indices['NDMI'],
                                       self.rutas_indices['NDVI'])