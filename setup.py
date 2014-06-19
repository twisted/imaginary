from epsilon.setuphelper import autosetup

import versioneer
versioneer.vcs = "git"
versioneer.versionfile_source = "imaginary/_version.py"
versioneer.versionfile_build = "imaginary/_version.py"
versioneer.tag_prefix= ""
versioneer.parentdir_prefix = "Imaginary-"

with open("README.rst") as fObj:
    readme = fObj.read()

distobj = autosetup(
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
    install_requires=[
        "twisted>=14.0.0",
        "epsilon>=0.7.0",
        "characteristic>=0.1.0",
        "axiom>=0.7.1",

        # Nevow is a dependency via Mantissa but Mantissa doesn't declare it in
        # `install_requires`.  So we'll declare it here to make things go more
        # smoothly until Mantissa gets fixed.
        "nevow>=0.10.0",

        # Likewise.
        "pytz", "pyasn1>=0.1.7",

        # Likewise.  PyCrypto has a history of breaking Conch in new releases
        # so pin it.
        "PyCrypto==2.6",

        "mantissa>=0.7.0",
        ],
    extras_require={
        "doc": ["sphinx>=1.2.2"],
        },
    )
