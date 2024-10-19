import codecs
import os

from setuptools import find_packages, setup

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.0.0'
DESCRIPTION = 'A sao shen library'
LONG_DESCRIPTION = 'The brother version of the Drissionpage library, SaossionPage, is referred to as Sao Shen for short.'

# Setting up
setup(
    name="SaossionPage",

    version=VERSION,
    author="sao shen",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'DrissionPage',
        'colorama',
        
    ],
    keywords=['python', 'menu', 'saoshen', 'windows', 'SaossionPage', 'linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)