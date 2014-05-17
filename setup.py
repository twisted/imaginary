from epsilon.setuphelper import autosetup

import versioneer
versioneer.vcs = "git"
versioneer.versionfile_source = "imaginary/_version.py"
versioneer.versionfile_build = "imaginary/_version.py"
versioneer.tag_prefix= ""
versioneer.parentdir_prefix = "Imaginary-"

with open("README.txt") as fObj:
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
        "Topic :: Terminals"])
