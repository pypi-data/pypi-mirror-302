from setuptools import find_packages, setup

long_description = "".join(
    [
        "PAC-Bayes learning routines\n",
        "This package provides implementations of PAC-Bayes learning routines ",
        "Note: faiss-cpu version is currently pinned to 1.7.3 for security.",
        "We plan to allow more versions in ulterior version of the package."
    ]
)

setup(
    name="picpacbayes",
    version="0.0.0.0",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="PAC-Bayes learning routines",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "apicutils>=0.0.3",
        "picoptim",
        "picproba",
        "pandas",
        "faiss-cpu",
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
