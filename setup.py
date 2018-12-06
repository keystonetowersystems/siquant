import os.path as path

from setuptools import find_packages, setup


def readme():
    filepath = path.join(path.dirname(path.realpath(__file__)), "README.rst")
    with open(filepath) as f:
        return f.read()


PROJECT_URLS = {
    "Documentation": "https://siquant.readthedocs.io/",
    "Bug Tracker": "https://github.com/keystonetowersystems/siquant/issues",
    "Source Code": "https://github.com/keystonetowersystems/siquant",
}
KEYWORDS = ["SI", "units", "dimensional analysis", "quantities"]


INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {"docs": ["sphinx", "numpy"], "tests": ["coverage", "pytest", "numpy"]}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["docs"] + EXTRAS_REQUIRE["tests"] + ["pre-commit"]
)


setup(
    name="siquant",
    version="4.0.0b11",
    description="Dimensional Analysis and Unit Tracking Library",
    long_description=readme(),
    url="https://github.com/keystonetowersystems/siquant",
    project_urls=PROJECT_URLS,
    keywords=KEYWORDS,
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
