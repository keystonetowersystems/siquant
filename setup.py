from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {"docs": ["sphinx"], "tests": ["coverage", "pytest"]}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["docs"] + EXTRAS_REQUIRE["tests"] + ["pre-commit"]
)


setup(
    name="siquant",
    version="3.0.2",
    description="SI units and quantities library",
    long_description=readme(),
    long_description_content_type="text/markdown",
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
