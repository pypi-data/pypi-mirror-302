#!/usr/bin/env python3

"""
setup.py file for python mapper
"""

from distutils.core import setup
import re
import platform

def ver():
    if platform.uname()[0] == 'Windows':
        # Parse version out of configure.ac
        versionPattern = re.compile("(?<=\[LIBMAPPER_VERSION],\[)(.*?)(?=])")
        for i, line in enumerate(open('../../configure.ac')):
            for match in re.finditer(versionPattern, line):
                version = match.group(0)
                print("Found libmapper version: %s" % version)
    else:
        version = '2.4.12.7+ge8a2087c'
    match = re.compile(r'(\d+)\.(\d+)\.(\d+)\.?(\d*)\+?.*').match(version)
    if match:
        if match.groups()[3]:
            return '{0}.{1}.{2}.dev{3}'.format(*[g or "" for g in match.groups()])
        else:
            return '{0}.{1}.{2}'.format(*[g or "" for g in match.groups()])
    else:
        return version

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = _bdist_wheel.get_tag(self)
            # We don't contain any python source
            python, abi = 'py3', 'none'
            return python, abi, plat
except ImportError:
    bdist_wheel = None

if platform.uname()[0] == 'Windows':
    packages = ["libmapper.dll", "liblo.dll", "zlib.dll"]
else:
    packages = ["libmapper.dylib"]
setup (name         = 'libmapper',
       version      = ver(),
       author       = "libmapper.org",
       author_email = "dot_mapper@googlegroups.com",
       url          = "http://libmapper.org",
       description  = "A library for representing input and output signals on a network and allowing arbitrary 'mappings' to be dynamically created between them.",
       long_description_content_type = "text/markdown",
       readme       = "README.md",
       license      = "GNU LGPL version 2.1 or later",
       packages     = ["src/libmapper"],
       package_data = {"libmapper": packages},
       cmdclass     = {
        'bdist_wheel': bdist_wheel,
       } if platform.uname()[0] != 'Linux' else {},
)
