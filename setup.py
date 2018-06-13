import os
from setuptools import setup, find_packages

PACKAGE_NAME = "CMIP6_json_data_citation_generator"
AUTHOR = "Zebedee Nicholls"
AUTHOR_EMAIL = "zebedee.nicholls@climate-energy-college.org"
DESCRIPTION = "Package to generate json files for the CMIP6 data citation system from filenames and a simple yaml file"

VERSION = "1.0.0"

def read(fname):
    """
    Read a file

    Thanks Jared Lewis :)
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license='MIT License',
    packages=find_packages(exclude=["tests"]),
    long_description=read('README.md'),
    url='https://gitlab.com/znicholls/CMIP6_data_file_renaming',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',

        'Programming Language :: Python :: 3',

        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science'
    ],
    keywords='CMIP6 climate reformatting',
)
