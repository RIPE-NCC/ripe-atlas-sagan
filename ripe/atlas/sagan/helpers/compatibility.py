"""
We put stuff here to help cope with differences between Python versions.
"""

try:
    string = basestring  # Python2
except NameError:
    string = str  # Python3

