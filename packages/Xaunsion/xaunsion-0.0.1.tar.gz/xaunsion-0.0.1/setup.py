from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'This name is reserve for Xaunsion.com for future'

# Setting up
setup(
    name="Xaunsion",
    version=VERSION,
    author="Xaunsion",
    author_email="<contact@xaunsion.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'Xaunsion'],
    classifiers=[
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)