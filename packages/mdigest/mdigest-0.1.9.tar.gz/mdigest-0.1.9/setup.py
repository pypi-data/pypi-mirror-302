from setuptools import setup, find_packages

VERSION = '0.1.9'
DESCRIPTION = 'Best practices made easy for analysis of correlated motions from molecular dynamics simulations.'
LONG_DESCRIPTION = 'MDiGest is a best-practices-made-easy Python package that handles the most common issues in ' \
                   'the network-based analysis of correlated motions from molecular dynamics simulations.'

setup(
    name="mdigest",
    version=VERSION,
    author="Federica Maschietto, Brandon Allen",
    author_email="<federica.maschietto@gmail.com>, <brandon.allen@yale.edu>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy>=1.21',
                      'numba',
                      'scipy',
                      'python-louvain==0.15',
                      'pandas',
                      'seaborn',
                      'mdtraj',
                      'MDAnalysis',
                      'silx',
                      'nglview',
                      'networkx'],

    keywords=[
        'python',
        'correlation',
        'molecular dynamics',
        'MD trajectory analysis',
        'correlated motions',
        'network analysis',
        'community network'
    ],
    url="https://github.com/fmaschietto/MDiGest",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
