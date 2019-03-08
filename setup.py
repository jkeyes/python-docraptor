# python-docraptor
# Copyright (C) 2011 John Keyes
# http://jkeyes.mit-license.org/

from setuptools import find_packages
from setuptools import setup

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="python-docraptor",
    version='1.2.3',
    description="Doc Raptor API wrapper",
    long_description=LONG_DESCRIPTION,
    author="John Keyes",
    author_email="john@keyes.ie",
    license="MIT License",
    url="http://github.com/jkeyes/python-docraptor",
    keywords='DocRaptor pdf python',
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"]
)
