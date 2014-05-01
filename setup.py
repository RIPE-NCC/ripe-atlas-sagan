import os
import sys
from setuptools import setup

name = "ripe.atlas.sagan"
version = open(os.path.join("ripe", "atlas", "sagan", "version")).read().strip()
install_requires = [
    "arrow>=0.4.2",
    "python-dateutil>=2.2",
    "pytz>=2014.2",
]

# pyOpenSSL support is flakey on some systems (I'm looking at you Apple)
if "SAGAN_WITHOUT_SSL" not in os.environ:
    install_requires.append("pyOpenSSL==0.13")

# Like pyOpenSSL, dnspython might be problematic for some
if "SAGAN_WITHOUT_DNS" not in os.environ:
    if sys.version_info < (3, 0):
        install_requires.append("dnspython>=1.11.1")
    else:
        install_requires.append("dnspython3>=1.11.1")

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=name,
    version=version,
    packages=["ripe", "ripe.atlas", "ripe.atlas.sagan"],
    namespace_packages=["ripe", "ripe.atlas"],
    include_package_data=True,
    license="GPLv3",
    description="A parser for RIPE Atlas measurement results",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
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
