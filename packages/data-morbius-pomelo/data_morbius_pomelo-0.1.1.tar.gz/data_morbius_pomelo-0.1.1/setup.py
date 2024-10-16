from setuptools import setup, find_packages

setup(
    name='data_morbius_pomelo',  # Nombre del paquete
    version='0.1.1',  # Versión inicial
    description='Funciones cross data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='bruno',
    author_email='bruno.iungano@pomelo.la',
    url='https://github.com/pomelo-la/infra-data-utilities',
    license='MIT',
    packages=find_packages(),  # Encuentra todos los paquetes automáticamente
    install_requires=[  # Dependencias
        'requests',
        'numpy',
        # Agrega más si es necesario
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python
)