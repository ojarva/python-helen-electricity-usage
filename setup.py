from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='helen_electricity_usage',
    version='0.1.1',
    description='Small library for scraping electricity usage information from Helsingin Energia website',
    long_description=long_description,
    url='https://github.com/ojarva/python-helen-electricity-usage',
    author='Olli Jarva',
    author_email='olli@jarva.fi',
    license='BSD',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='electricity helen',
    packages=["helen_electricity_usage"],
    install_requires=['requests>=2.5.1', 'beautifulsoup4>=4.4.1'],

    extras_require={
        'dev': ['twine', 'wheel'],
    },
)
