import os
import sys
from setuptools import setup

name = "ripe.atlas.sagan"
version = open(os.path.join("ripe", "atlas", "sagan", "version")).read().strip()
install_requires = [
    "arrow>=0.4.2",
    "python-dateutil>=2.2",
    "pytz>=2014.2",
    "IPy",
]

# pyOpenSSL support is flakey on some systems (I'm looking at you Apple)
if "SAGAN_WITHOUT_SSL" not in os.environ:
    install_requires.append("pyOpenSSL>=0.12")
    install_requires.append("pyOpenSSL<0.14")

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Get the long description from README.md
long_description = None
with open(os.path.join(os.path.dirname(__file__), "README.md")) as description:
    long_description = description.read()

setup(
    name=name,
    version=version,
    packages=["ripe", "ripe.atlas", "ripe.atlas.sagan"],
    namespace_packages=["ripe", "ripe.atlas"],
    include_package_data=True,
    license="GPLv3",
    description="A parser for RIPE Atlas measurement results",
    long_description=long_description,
    url="https://github.com/RIPE-NCC/ripe.atlas.sagan",
    download_url="https://github.com/RIPE-NCC/ripe.atlas.sagan",
    author="Daniel Quinn",
    author_email="dquinn@ripe.net",
    maintainer="Daniel Quinn",
    maintainer_email="dquinn@ripe.net",
    install_requires=install_requires,
    scripts=[
        "scripts/parse_abuf"
    ],
    classifiers=[
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
