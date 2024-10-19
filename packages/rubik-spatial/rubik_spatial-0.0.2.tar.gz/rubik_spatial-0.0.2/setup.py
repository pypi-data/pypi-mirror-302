#this is a setup.py file
from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = "Python package for rapid spatial alignment of spatial transcriptomic datasets"
LONG_DESCRIPTION = "Python package for rapid spatial alignment of spatial transcriptomic datasets"

setup(
    name="rubik_spatial",
    version=VERSION,
    author="Bence Kover",
    author_email="<kover.bence@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-image",
        "scanpy",
        "squidpy",
        "tqdm",
        "matplotlib",
        "Pseudovisium",
    ],

    keywords=['spatial', 'transcriptomics', 'visium', 'xenium', 'rubik'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X"
    ]
)

