from setuptools import setup, find_packages

import versioneer
versioneer.vcs = "git"
versioneer.versionfile_source = "imaginary/_version.py"
versioneer.versionfile_build = "imaginary/_version.py"
versioneer.tag_prefix= ""
versioneer.parentdir_prefix = "Imaginary-"

with open("README.rst") as fObj:
    readme = fObj.read()

distobj = setup(
    name="Imaginary",
    version=versioneer.get_version(),
    maintainer="Divmod, Inc.",
    maintainer_email="support@divmod.org",
    url="http://divmod.org/trac/wiki/DivmodImaginary",
    license="MIT",
    platforms=["any"],
    description=readme,
    cmdclass=versioneer.get_cmdclass(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Terminals"],
    packages=find_packages() + ['axiom.plugins', 'xmantissa.plugins'],
    install_requires=[
        "twisted>=14.0.0",
        "epsilon>=0.7.0",
        "attrs",
        "axiom>=0.7.1",
        "mantissa>=0.8.0",
        ],
    extras_require={
        "doc": ["sphinx>=1.2.2"],
        },
    )
