setupdict= {
    'name': 'peerindex',
    'version': '0.1',
    'author': 'Guido van Oorschot',
    'url': 'http://dev.peerindex.com/',
    'description': 'A Python interface for the PeerIndex API.',
    'long_description': 'A Python interface for the PeerIndex API.',
    'py_modules': ['PeerIndexPy'],
    }

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(**setupdict)
