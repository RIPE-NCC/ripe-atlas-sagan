import os
from setuptools import setup

__version__ = None
exec(open("ripe/atlas/sagan/version.py").read())

name = "ripe.atlas.sagan"
install_requires = [
    "python-dateutil",
    "pytz",
    "IPy",
]

tests_require = ["nose"]

# pyOpenSSL support is flaky on some systems (I'm looking at you Apple)
if "SAGAN_WITHOUT_SSL" not in os.environ:
    install_requires.append("pyOpenSSL")

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

readme_path = os.path.join(os.path.dirname(__file__), "README.rst")
changelog_path = os.path.join(os.path.dirname(__file__), "Changelog.rst")

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
            author="Daniel Quinn",
            author_email="dquinn@ripe.net",
            maintainer="Daniel Quinn",
            maintainer_email="dquinn@ripe.net",
            install_requires=install_requires,
            tests_require=tests_require,
            extras_require={
                "fast": ["ujson"],
                "doc": ["sphinx"]
            },
            test_suite="nose.collector",
            scripts=[
                "scripts/parse_abuf"
            ],
            classifiers=[
                "Operating System :: POSIX",
                "Operating System :: Unix",
                "Programming Language :: Python",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.1",
                "Programming Language :: Python :: 3.2",
                "Programming Language :: Python :: 3.3",
                "Programming Language :: Python :: 3.4",
                "Topic :: Internet :: WWW/HTTP",
            ],
        )
