"""
Setup script for Django Cruder package
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-cruder',
    version='1.0.0',
    author='Django Cruder Team',
    author_email='info@cruder.dev',
    description='Advanced CRUD operations for Django with multiple CSS framework support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/django-cruder/django-cruder',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'cruder': [
            'templates/cruder/*.html',
            'templates/cruder/*/*.html',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    install_requires=[
        'Django>=3.2',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-django',
            'black',
            'flake8',
            'coverage',
        ],
    },
    keywords='django crud forms bootstrap bulma css framework',
    project_urls={
        'Bug Reports': 'https://github.com/django-cruder/django-cruder/issues',
        'Source': 'https://github.com/django-cruder/django-cruder',
        'Documentation': 'https://django-cruder.readthedocs.io/',
    },
)