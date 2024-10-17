#!/usr/bin/env python
# Compile and upload on pip:
#    python3 -m pip install --upgrade build
#    python3 -m pip install --upgrade twine
#    python3 -m twine upload dist/*

from setuptools import setup, find_namespace_packages

setup(
    name='cima-goes-aio',
    version='0.1.b11',
    description='GOES-16 File Processing with asyncio and multiprocessing',
    author='Fido Garcia',
    author_email='garciafido@gmail.com',
    package_dir={'': 'src'},
    url='https://github.com/garciafido/cima-goes-aio',
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    python_requires='>=3.12',
    license='MIT',
    package_data={'': ['*.json', '*.cpt']},
    data_files = [("", ["LICENSE"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    __token__='garciafido',
)