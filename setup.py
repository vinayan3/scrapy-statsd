"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scrapy-statsd',
    version='1.0.0a1',
    description='Publish Scrapy stats to statsd',
    long_description=long_description,
    url='https://github.com/vinayan3/scrapy-statsd',
    author='Vinay Anantharaman',
    author_email='dev@null.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='scrapy stats',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'Scrapy>=1.0.5',
        'statsd==3.2.1'
    ],
    extras_require={
        'dev': [],
        'test': ['mock==1.3.0'],
    },
)
