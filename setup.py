#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='rename',
    version='0.1.0',

    description='A sample Python project',
    url='https://github.com/hscup/xmp-based-rename',
    author='heyuno',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='script, utility',
    install_requires=['Pillow==4.3.0'],
    scripts=['rename.py'],
    entry_points={
        'console_scripts': [
            'rename=rename:main',
        ],
    },
) 