import os
from setuptools import setup, find_packages


def read(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, mode='r', encoding='utf-8') as f:
        return f.read()


setup(
    name='external_sort',
    description='BERT for NER using catalyst',
    author='Dmitry Kryuchkov',
    author_email='xelibrion@gmail.com',
    url='https://github.com/xelibrion/sort-large-files',
    packages=find_packages(),
    install_requires=read('requirements.txt').splitlines(),
    entry_points={
        'console_scripts': [
            'sort-large-files = external_sort.__main__:main',
        ],
    },
    zip_safe=True,
)
