import os
import sys
from setuptools import setup

name = "ripe.atlas.sagan"
version = "0.1a"
install_requires = [
    "arrow>=0.4.2",
    "pyOpenSSL>=0.14",
    "python-dateutil>=2.2",
    "pytz>=2014.2",
]
if sys.version_info.major < 3:
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
    url="https://github.com/RIPE-NCC/sagan",
    download_url="https://github.com/RIPE-NCC/sagan",
    author="Daniel Quinn",
    author_email="dquinn@ripe.net",
    maintainer="Daniel Quinn",
    maintainer_email="dquinn@ripe.net",
    install_requires=install_requires,
    classifiers=[
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
)

