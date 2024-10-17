from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

NAME = 'planetool'
VERSION = '0.1'
DESCRIPTION = 'planetool, manyetik alanlar, gelgit kuvvetleri, ısı akışı ve daha fazlasını içeren gezegen bilim hesaplamaları için tasarlanmış bir Python sınıfıdır. Bu sınıf, manyetik alanlar, Coriolis kuvvetleri, gelgit kuvvetleri, dalga enerjisi, basınç ve Gibbs enerjisi gibi fiziksel fenomenleri tanımlamak için matematiksel modelleri içeren geniş bir gezegen fiziği işlevleri yelpazesi sunar.'
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
URL = 'https://github.com/GizemSena/planetool'
AUTHOR = 'Gizem Sena Çengel'
AUTHOR_EMAIL = 'gizemsenac@gmail.com'
LICENSE = 'MIT'
KEYWORDS = 'Exoplanet,physics'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    keywords=KEYWORDS,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12'
    ],
    py_modules=["planetool"]
)