import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='siquant',
    version='2.4.0',
    description='SI units and quantities library',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/keystonetowersystems/siquant',
    author='Greg Echelberger',
    author_email='greg@keystonetowersystems.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=[],
    tests_require=[ "pytest>=3.8", "pytest-cov>=2.6.0" ],
    setup_requires=[
        'tox',
        'coverage>=4.5'
    ],
    cmdclass = {
        'test' : PyTest
    },
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
)
