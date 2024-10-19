from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='peruscp',
    version='0.0.2.1',
    license='MIT',
    description='Es un paquete que realiza una solicitud a eldni.com extrayendo todos los datos a consultar, util para bots, APIS, Paginas WEB, son datos basicos de Reniec.',
    long_description=README,
    long_description_content_type="text/markdown",
    author='bapinzon',
    packages=find_packages(),
    install_requires=['requests','BeautifulSoup'],
    author_email="bryanpinzon469@gmail.com",
    url='https://github.com/bapinzon/peruscp'
)