import os

from setuptools import find_packages, setup

loc_dir = os.path.realpath(os.path.dirname(__file__))

with open(os.path.join(loc_dir, "requirements.txt"), "r", encoding="utf-8") as f:
    # Make sure we strip all comments and options (e.g "--extra-index-url")
    # that arise from a modified pip.conf file that configure global options
    requires = []
    for line in f:
        req = line.split("#", 1)[0].strip()
        if req and not req.startswith("--"):
            requires.append(req)

setup(
    name="anaerodig",
    version="0.0.1",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="Anaerobic Digestion models, in python",
    packages=find_packages(),
    install_requires=requires,
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
