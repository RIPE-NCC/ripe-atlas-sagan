#!/bin/sh

# This is a generic build-debian-packages-script and is also capable to build
# binary debian packages (which is not needed in this case).
# The installable .deb file is located in the directory above
#
# prerequisites to build debian/ubuntu packages
# sudo apt-get install python-setuptools debhelper

export DEBFULLNAME="RIPE-NCC AutoBuilder"
export DEBEMAIL="dquinn@ripe.net"

# set VERSION before invoking this script
if [ -z "$VERSION" ]; then
  echo 'Please set $VERSION'           >&2
  echo "e.g. export VERSION=1.1.7; $0" >&2
  exit 1
fi

# check if all dependencies are installed
dpkg -l debhelper python-setuptools python-zope.ucol > /dev/null
RETVAL=$?
if [ "$RETVAL" -ne 0 ]; then
  echo 'Please install python-setuptools debhelper'       >&2
  echo 'sudo apt-get install python-setuptools debhelper' >&2
  exit 1
fi

# places the .deb file in the directory above
DISTDIR=${DISTDIR:=.}

set -e
set -x

cd $DISTDIR

# create an empty debian/changelog
# CHANGES.rst has not the format debian/changelog requires
mkdir -p debian
cat > debian/changelog << EOF
ripe.atlas.sagan (${VERSION}) unstable; urgency=medium

  * Automatic build. For changlog see CHANGES.rst

 -- ${DEBFULLNAME} <${DEBEMAIL}>  $(date -R)
EOF

# create debian/control file
cat > debian/control << EOF
Source: ripe.atlas.sagan
Section: python
Priority: optional
Standards-Version: ${VERSION}
Maintainer: ${DEBFULLNAME} <${DEBEMAIL}>
Origin: RIPE-NCC
Build-Depends: debhelper (>= 9)
X-Python-Version: >= 2.5
Homepage: https://github.com/RIPE-NCC/ripe.atlas.sagan/

Package: python-ripe.atlas.sagan
Architecture: any
Depends: \${python:Depends}, python-openssl, python-ipy, python-tz, python-dateutil
Replaces: python-ripe.atlas.sagan
Suggests: python-ripe.atlas.cousteau, python-ripe.atlas.tools
Description: Parsing library for RIPE Atlas measurement results
 RIPE Atlas generates a lot of data, and the format of that data
 changes over time. Often you want to do something simple like fetch
 the median RTT for each measurement result between date X and date
 Y. Unfortunately, there are dozens of edge cases to account for
 while parsing the JSON, like the format of errors and firmware
 upgrades that changed the format entirely.
 .
 To make this easier for our users (and for ourselves), we wrote an
 easy to use parser that's smart enough to figure out the best
 course of action for each result, and return to you a useful,
 native Python object. 
EOF

# create debian/rules file
cat > debian/rules << EOF
#!/usr/bin/make -f
# See debhelper(7) (uncomment to enable)
# output every command that modifies files on the build system.
#DH_VERBOSE = 1

# see EXAMPLES in dpkg-buildflags(1) and read /usr/share/dpkg/*
DPKG_EXPORT_BUILDFLAGS = 1
include /usr/share/dpkg/default.mk

# see FEATURE AREAS in dpkg-buildflags(1)
#export DEB_BUILD_MAINT_OPTIONS = hardening=+all

# see ENVIRONMENT in dpkg-buildflags(1)
# package maintainers to append CFLAGS
#export DEB_CFLAGS_MAINT_APPEND  = -Wall -pedantic
# package maintainers to append LDFLAGS
#export DEB_LDFLAGS_MAINT_APPEND = -Wl,--as-needed

# main packaging script based on dh7 syntax
%:
        dh \$@
EOF

# debian/rule must be executable
chmod +x debian/rules

# create debian/compat file
cat > debian/compat << EOF
9
EOF

# create debian/copyright file
cat > debian/copyright << EOF
Files: *
Copyright: 2015-2016 Daniel Quinn, Andreas Strikos
License: GPL-3

Files: debian/*
Copyright: 2016 Arsen Stasic
License: GPL-3

License: GPL-3
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, version 3 of the License.
 .
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.
 .
 On Debian systems, the complete text of the GNU General Public License
 version 3 can be found in the /usr/share/common-licenses/GPL-3 file.
EOF

# build the .deb package
DH_OPTIONS=--parallel fakeroot debian/rules binary -d
dh_auto_build

# to remove debian package
rm -rf debian
