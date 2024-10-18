from setuptools import find_packages, setup

long_description = "".join(
    [
        "Optimisation routines\n",
        "This package provides abstract classes for Optimisation routines ",
        "and implementations of optimisation routines such as CMA-ES and Grid Search",
    ]
)

setup(
    name="picoptim",
    version="0.0.3",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="Optimisation routines and abstraction",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "apicutils>=0.0.3",
        "pandas",
        "scipy>=1.7.0",
        "numpy<=1.26",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
