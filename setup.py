import os
from setuptools import setup

__version__ = None
exec(open("ripe/atlas/sagan/version.py").read())

name = "ripe.atlas.sagan"
install_requires = [
    "python-dateutil",
    "pytz",
]

tests_require = ["nose"]

if "SAGAN_WITHOUT_SSL" not in os.environ:
    install_requires.append("cryptography")

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

readme_path = os.path.join(os.path.dirname(__file__), "README.rst")
changelog_path = os.path.join(os.path.dirname(__file__), "CHANGES.rst")

# Get the long description from README.md
with open(readme_path) as readme:
    with open(changelog_path) as changelog:
        setup(
            name="ripe.atlas.sagan",
            version=__version__,
            packages=["ripe", "ripe.atlas", "ripe.atlas.sagan"],
            namespace_packages=["ripe", "ripe.atlas"],
            include_package_data=True,
            license="GPLv3",
            description="A parser for RIPE Atlas measurement results",
            long_description="{readme}\n\n{changelog}".format(
                readme=readme.read(),
                changelog=changelog.read()
            ),
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
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.5",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Topic :: Internet :: WWW/HTTP",
            ],
        )
