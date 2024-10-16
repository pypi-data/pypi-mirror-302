from setuptools import find_packages, setup

setup(
    name="anaerodig",
    version="0.0.5",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="Anaerobic Digestion models, in python",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scipy>=1.7.0",
        "numpy<=1.26",
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
