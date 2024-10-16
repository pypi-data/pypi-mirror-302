from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A utility ETL library for internal development at NUDA'
LONG_DESCRIPTION = """cerberuslib is a robust ETL library designed for the NUDA team at Unimed SC. 
This library provides essential utilities for data extraction, transformation, and loading processes, 
streamlining workflows and enhancing data management capabilities.
"""

setup(
    name="cerberus-etl",
    version=VERSION,
    author="Gabriel Deglmann Kasten",
    author_email="gabriel.kasten@unimedsc.coop.br",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'pandas',
        'oracledb',
        'requests',
    ],
    keywords=['python', 'ETL', 'data pipeline', 'data stream', 'NUDA'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
