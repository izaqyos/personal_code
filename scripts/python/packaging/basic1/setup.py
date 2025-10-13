"""
To build a package for distribution:
python setup.py sdist

To build a binnary installer for windows:
python setup.py bdist_wininst
"""
from distutils.core import setup
setup(name='foo',
      version='1.0',
      py_modules=['foo'],
      )
