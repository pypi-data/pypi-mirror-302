# clasificador_base.py
class ClasificadorBase:
    def __init__(self, rutas_indices):
        self.rutas_indices = rutas_indices

    def clasificar(self):
        raise NotImplementedError("Subclasses should implement this method")