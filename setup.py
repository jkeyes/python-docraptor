# python-docraptor
# Copyright (C) 2011 John Keyes
# http://jkeyes.mit-license.org/

from setuptools import find_packages
from setuptools import setup

setup(name="python-docraptor",
    version='1.0',
    description="Doc Raptor API wrapper",
    long_description=open('README.md').read(),
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