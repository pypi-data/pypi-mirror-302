import os

from setuptools import setup, find_packages

requirements = []
if os.path.isfile('requirements.txt'):
    with open('requirements.txt', 'r') as file_handler:
        requirements = file_handler.readlines()

setup(
    name='easyloader',
    version='1.0.1',
    author='Michael Peter Dunne',
    description='Easily turn DFs, Arrays, and H5 files into PyTorch DataLoaders.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages(include=['easyloader', 'easyloader.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
