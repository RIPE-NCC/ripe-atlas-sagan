from os.path import abspath, dirname, join
from os import environ
from setuptools import setup

__version__ = None
exec(open("ripe/atlas/sagan/version.py").read())

name = "ripe.atlas.sagan"
install_requires = [
    "python-dateutil",
    "pytz",
]

tests_require = ["nose"]

if "SAGAN_WITHOUT_SSL" not in environ:
    install_requires.append("cryptography")

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
    tests_require=tests_require,
    extras_require={
        "fast": ["ujson"],
        "doc": ["sphinx"]
    },
    test_suite="nose.collector",
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
