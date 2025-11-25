import os
from os.path import abspath, dirname, join
from setuptools import setup

__version__ = None
exec(open("ripe/atlas/sagan/version.py").read())

name = "ripe.atlas.sagan"
install_requires = [
    "python-dateutil",
    "pytz",
    "cryptography",
]

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Get proper long description for package
current_dir = dirname(abspath(__file__))
description = open(join(current_dir, "README.rst")).read()
changes = open(join(current_dir, "CHANGES.rst")).read()
long_description = "\n\n".join([description, changes])

setup(
    name="ripe.atlas.sagan",
    version=__version__,
    packages=["ripe", "ripe.atlas", "ripe.atlas.sagan"],
    namespace_packages=["ripe", "ripe.atlas"],
    include_package_data=True,
    license="GPLv3",
    description="A parser for RIPE Atlas measurement results",
    long_description=long_description,
    url="https://github.com/RIPE-NCC/ripe.atlas.sagan",
    download_url="https://github.com/RIPE-NCC/ripe.atlas.sagan",
    author="The RIPE Atlas Team",
    author_email="atlas@ripe.net",
    maintainer="The RIPE Atlas Team",
    maintainer_email="atlas@ripe.net",
    install_requires=install_requires,
    extras_require={
        "fast": ["ujson"],
        "doc": ["sphinx"]
    },
    classifiers=[
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
