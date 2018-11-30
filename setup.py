import versioneer

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


PACKAGE_NAME = "cmip6-data-citation-generator"
AUTHOR = "Zebedee Nicholls"
EMAIL = "zebedee.nicholls@climate-energy-college.org"
URL = "https://github.com/znicholls/CMIP6-json-data-citation-generator"

DESCRIPTION = (
    "CMIP6 auxillary tool to generate data citation files from output data files"
)
README = "README.rst"

SOURCE_DIR = "src"

with open(README, "r") as readme_file:
    README_TEXT = readme_file.read()


class CMIP6DataCitationGenerator(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        pytest.main(self.test_args)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": CMIP6DataCitationGenerator})

setup(
    name=PACKAGE_NAME,
    version=versioneer.get_version(),
    description=DESCRIPTION,
    long_description=README_TEXT,
    long_description_content_type="text/x-rst",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license="2-Clause BSD License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    keywords=["netcdf", "python", "climate", "cmip6"],
    packages=find_packages(SOURCE_DIR),  # no tests/docs in `src` so don't need exclude
    package_dir={"": SOURCE_DIR},
    # include_package_data=True,
    install_requires=["PyYAML", "marshmallow==3.0.0b20", "httplib2", "netcdf-scm"],
    extras_require={
        "docs": ["sphinx", "sphinx_rtd_theme"],
        "test": ["codecov", "pytest-cov", "pytest"],
        "deploy": ["twine", "setuptools", "wheel", "flake8", "black", "versioneer"],
    },
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "generate-cmip6-citation-files=cmip6_data_citation_generator.cli:generate",
            "upload-cmip6-citation-files=cmip6_data_citation_generator.cli:upload",
        ]
    },
)
