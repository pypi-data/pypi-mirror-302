from setuptools import setup, find_packages

setup(
    name='peruscp',
    version='0.0.1',
    license='MIT',
    description='Es un paquete que realiza una solicitud a eldni.com extrayendo todos los datos a consultar, util para bots, APIS, Paginas WEB, son datos basicos de Reniec.',
    author='bapinzon',
    packages=find_packages(),
    install_requires=['requests','BeautifulSoup'],
    author_email="bryanpinzon469@gmail.com",
    url='https://github.com/bapinzon/peruscp'
)