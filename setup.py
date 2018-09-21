from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='siquant',
    version='2.0.0.dev1',
    description='SI units and quantities library',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/keystonetowersystems/siquant',
    author='Greg Echelberger',
    author_email='greg@keystonetowersystems.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=[],
    python_requires='>=2.7',
    setup_requires=[
        "nose>=1.3.7"
    ],
    test_suite="nose.collector",
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
