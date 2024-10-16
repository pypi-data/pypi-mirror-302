"""
Este módulo contiene la clase ManejadorArgumentos, que maneja el análisis de argumentos de línea de comandos.

Clases:
    ManejadorArgumentos: Una clase para gestionar los argumentos de línea de comandos usando argparse.
"""

import argparse

class ManejadorArgumentos:
    def __init__(self):
        """
        Inicializa la clase ManejadorArgumentos y configura los argumentos del parser.

        Args:
            Ninguno
        """
        self.parser = argparse.ArgumentParser(description="Procesar carpetas de imágenes y ruta del polígono.")
        self.parser.add_argument('--carpeta_recortadas', type=str, help='Carpeta para imágenes recortadas')
        self.parser.add_argument('--carpeta_no_recortadas', type=str, help='Carpeta para imágenes no recortadas')
        self.parser.add_argument('--ruta_poligono', type=str, help='Ruta del archivo de polígono')
        self.parser.add_argument('--ruta_datos_ovitrampas', type=str, help='Ruta del archivo de datos de ovitrampas')
        self.args = self.parser.parse_args()

    def obtener_argumentos(self):
        """
        Obtiene los argumentos parseados.

        Returns:
            Namespace: Un objeto Namespace con los argumentos parseados.
        """
        return self.args