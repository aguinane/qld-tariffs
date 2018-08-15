""" A setuptools based setup module.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='qldtariffs',
    packages=['qldtariffs'],
    include_package_data=True,
    version='0.2',
    description='Calculate the energy costs for QLD tariffs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='aguinane',
    author_email='alexguinane@gmail.com',
    url='https://github.com/aguinane/qld-tariffs',
    keywords=['energy', 'qld', 'tariff'],
    classifiers=[],
    license='MIT',
    install_requires=[
        'pytoml',
        'energy-shaper>=0.1.1'
    ],
)
