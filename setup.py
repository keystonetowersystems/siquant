import os.path as path

from setuptools import find_packages, setup


def readme():
    filepath = path.join(path.dirname(path.realpath(__file__)), "README.rst")
    with open(filepath) as f:
        return f.read()


INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {"docs": ["sphinx"], "tests": ["coverage", "pytest"]}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["docs"] + EXTRAS_REQUIRE["tests"] + ["pre-commit"]
)


setup(
    name="siquant",
    version="3.0.5",
    description="SI units and quantities library",
    long_description=readme(),
    url="https://github.com/keystonetowersystems/siquant",
    author="Greg Echelberger",
    author_email="greg@keystonetowersystems.com",
    packages=find_packages(exclude=("tests",)),
    install_requires=INSTALL_REQUIRES,
    setup_requires=["tox"],
    extras_require=EXTRAS_REQUIRE,
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
