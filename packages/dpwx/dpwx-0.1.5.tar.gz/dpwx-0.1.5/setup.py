# coding=utf-8
from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.5'

setup(
    name='dpwx',
    version=VERSION,
    description='my package',
    packages=find_packages(),
    install_requires=['pymem'],
    package_data={'pywxdump': ['WX_OFFS.json']},
)
