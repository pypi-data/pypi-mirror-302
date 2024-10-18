from setuptools import find_packages, setup

long_description = "".join(
    [
        "PAC Bayes Meta Learning routines.",
    ]
)

setup(
    name="picmeta",
    version="0.0.1",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="PAC-Bayes meta Learning",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "apicutils>=0.0.3",
        "picproba",
        "picoptim>=0.0.3",
        "picpacbayes>=0.0.2",
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
