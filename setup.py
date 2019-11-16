import os
import unittest
from setuptools import setup, find_packages


def discover_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


def read(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, mode='r', encoding='utf-8') as f:
        return f.read()


setup(
    name='external_sort',
    description='Sorting of large files',
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
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    test_suite='setup.discover_tests',
)
