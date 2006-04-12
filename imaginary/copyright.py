
# <major> <minor> <patch> <alpha | pre | final | zzz> <iteration>
version_info = (0, 1, 0, 'alpha', 0)

# Sortable version information.  This will always only
# increase from an older version to a newer version.
hexversion = (version_info[0] << 24 |
              version_info[1] << 16 |
              version_info[2] << 8 |
              ['alpha', 'pre', 'final', 'zzz'].index(version_info[3]) << 4 |
              version_info[4])

# Human-readable format
if version_info[3] == 'final':
    version = '%d.%d.%d%s' % version_info[:-1]
elif version_info[3] != 'zzz':
    version = '%d.%d.%d%s%d' % version_info
else:
    version = "SVN-trunk"

# Longer human-readable format
longversion= "Imaginary " + version
