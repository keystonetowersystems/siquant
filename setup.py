from setuptools import setup, find_packages

setup(
    name='siquant',
    version='1.0.0',
    description='SI units and quantities library',
    url='https://github.com/keystonetowersystems/siquant',
    author='Greg Echelberger',
    author_email='greg@keystonetowersystems.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=[],
    setup_requires=["nose==1.3.7"],
    test_suite="nose.collector",
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
