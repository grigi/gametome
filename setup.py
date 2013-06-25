import os
from setuptools import setup, find_packages

# This is to disable the 'black magic' surrounding versioned repositories... Terrible!
from setuptools.command import sdist
del sdist.finders[:]

setup(
    name='gametome',
    version = '0.1.0',
    description='Project for gametome',
    long_description=open('README.md', 'rt').read(),
    author='',
    author_email='',
    url='',
    zip_safe = False,

    # Dependencies
    install_requires = [
        'django >=1.5',
        'django-taggit',
        'django-allauth >=0.10',
        'django-haystack',
        'Whoosh',
        'html2text',
        'pybbm',
        #'sorl.thumbnail',
        'django-pure-pagination',
        'django-galeria',
    ],
    dependency_links = [
    ],

    # Packages
    packages = find_packages(),
    include_package_data = True,

    # Scripts
    scripts = [
       'gametome/wsgi_prod.py',
    ],
)

