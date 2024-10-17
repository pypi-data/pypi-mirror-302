from setuptools import setup, find_packages
import codecs
import os

from pathlib import Path
this_directory = Path(__file__).parent

VERSION = '0.0.2'
DESCRIPTION = 'A Python Tool Package'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="pryttier",
    version=VERSION,
    author="HussuBro010 (Hussain Vohra)",
    author_email="<hussainv2807@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'pandas'],
    keywords=['python', 'graphing', 'math', 'tools', 'colors'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
