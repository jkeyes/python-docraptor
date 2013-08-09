# python-docraptor
# Copyright (C) 2011 John Keyes
# http://jkeyes.mit-license.org/

from setuptools import setup, find_packages

setup(name="python-docraptor",
    version='1.1',
    description="Doc Raptor API wrapper",
    long_description=open('README.md').read(),
    author="John Keyes",
    author_email="john@keyes.ie",
    license="MIT License",
    url="http://github.com/jkeyes/python-docraptor",
    keywords='DocRaptor pdf python',
    classifiers=[],
    use_2to3=True,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"]
)
