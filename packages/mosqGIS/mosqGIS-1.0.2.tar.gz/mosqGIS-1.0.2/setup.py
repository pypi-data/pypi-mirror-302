import os.path

from setuptools import setup, find_packages

from setuptools import setup, find_packages
import os

# Función para leer las dependencias desde requirements.txt
def parse_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

setup(
    name="mosqGIS",  # Nombre del proyecto
    version="1.0.2",
    author="Justo Garcia",
    author_email="justogarciapc@gmail.com",  # Cambia esto a tu email
    description="Pipeline para la extracción de información de imágenes satelitales y datos de ovitrampas",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/justog220/mosqGIS",  # URL del repositorio
    packages=find_packages(),
    install_requires=[
        "matplotlib==3.9.2",
        "numpy==2.1.2",
        "pandas==2.2.3",
        "rasterio==1.3.10",
        "scikit_learn==1.5.2",
    ],  # Carga las dependencias desde requirements.txt
    extras_require={
        "dev": [
            "pytest>=6.2.4",  # Dependencias opcionales para desarrollo
            "sphinx>=4.0.2",
            "black>=21.7b0",
        ],
    },
    entry_points={
        'console_scripts': [
            'mosqGIS=mosqGIS.main:main',  # Ejecuta el pipeline desde la línea de comandos
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True,  # Incluye archivos no Python como datos
)
