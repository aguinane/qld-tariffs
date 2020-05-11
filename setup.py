""" A setuptools based setup module.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the version information
about = {}
ver_path = path.join(here, "qldtariffs", "version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), about)

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]
setup_requirements = ["pytest-runner"]
test_requirements = ["pytest>=3","pytest-cov"]

setup(
    name="qldtariffs",
    version=about["__version__"],
    description="Calculate the energy costs for QLD tariffs",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alex Guinman",
    author_email="alex@guinman.id.au",
    url="https://github.com/aguinane/qld-tariffs",
    keywords=["energy", "qld", "tariff"],
    classifiers=[],
    python_requires=">=3.6",
    install_requires=install_requires,
    dependency_links=dependency_links,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    license="MIT",
)
