import os

from setuptools import setup, find_packages

requirements = []
if os.path.isfile('requirements.txt'):
    with open('requirements.txt', 'r') as file_handler:
        requirements = file_handler.readlines()

setup(
    name='codeine',
    version='0.0.0',
    author='Gabriel Duran, Michael Peter Dunne',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages(include=['codeine', 'codeine.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
