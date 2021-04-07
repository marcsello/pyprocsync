#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['redis~=3.5.3', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Marcell Pünkösd",
    author_email='punkosdmarcell@rocketmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Synchronize events between processes over the network",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyprocsync',
    name='pyprocsync',
    packages=find_packages(include=['pyprocsync', 'pyprocsync.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcsello/pyprocsync',
    project_urls={
        "Documentation": "https://pyprocsync.readthedocs.io/",
        "Code": "https://github.com/marcsello/pyprocsync",
        "Issue tracker": "https://github.com/marcsello/pyprocsync/issues",
    },
    version='0.1.0',
    zip_safe=False,
)
