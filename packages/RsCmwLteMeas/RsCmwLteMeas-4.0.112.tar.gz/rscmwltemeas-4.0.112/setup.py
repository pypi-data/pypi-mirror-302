import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setup(
    name="RsCmwLteMeas",
    version="4.0.112",
    description="CMW LTE Measurement Remote-control module",
    long_description=README,
    long_description_content_type="text/x-rst",
    author="Rohde & Schwarz GmbH & Co. KG",
    copyright="Copyright © Rohde & Schwarz GmbH & Co. KG 2024",
    license="MIT",
    classifiers=['License :: OSI Approved :: MIT License',
                 'Intended Audience :: Developers',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: MacOS :: MacOS X',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.11',
                 'Programming Language :: Python :: 3.12'
                ],
    packages=(find_packages(include=['RsCmwLteMeas', 'RsCmwLteMeas.*'])),
    install_requires=['PyVisa>=1.13.0', 'typing-extensions>=4.0.0'],
    python_requires='>=3.8'
)