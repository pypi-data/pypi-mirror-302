from setuptools import find_packages, setup

long_description = "".join(
    [
        "Anaerobic Digestion models in Python\n",
        "This package structures AD models around configuration,",
        "feed, and initial state objects.\n",
        "Implementations of ADM1 and AM2 models are available in submodules",
        "'pyadm1' and 'pyam2'",
    ]
)

"""
Anaerobic Digestion models in Python
This package contains submodules 'pyadm1', 'pyam2' for ADM1 and AM2 packages respectively, as well as a d
"""

setup(
    name="anaerodig",
    version="0.0.6",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="Anaerobic Digestion models, in python",
    long_description=long_description,
    packages=["anaerodig"],
    package_dir={"anaerodig": "anaerodig"},
    package_data={"anaerodig": ["*/data/*.json", "*/data/*.csv"]},
    install_requires=[
        "pandas",
        "scipy>=1.7.0",
        "numpy<=1.26",
        "numba==0.58",
        "multiprocess>=0.70",
        "matplotlib>=3.7.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
