#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import os
import sys
import pambox


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', 'CHANGES.txt')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='pambox',
    version=pambox.__version__,
    url='https://bitbucket.org/achabotl/pambox',
    license='Modified BSD License',
    author='Alexandre Chabot-Leclerc',
    tests_require=['pytest'],
    install_requires=[],
    cmdclass={'test': PyTest},
    author_email='pambox@alex.alexchabot.net',
    description='A Python auditory modeling toolbox',
    long_description=long_description,
    packages=['pambox'],
    include_package_data=True,
    platforms='any',
    test_suite='pambox.test.test_pambox',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Alpha',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    extras_require={
        'testing': ['pytest'],
    }
)