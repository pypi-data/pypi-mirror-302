#!/usr/bin/env python3
#
# Copyright 2021-2024 NXP
# SPDX-License-Identifier: BSD-3-Clause
#
# NXP USBSIO Library - setup script
#

from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='libusbsio',
    version='2.1.13',
    description='Python wrapper around NXP LIBUSBSIO library',
    long_description_content_type="text/markdown",
    long_description=README,
    platforms="Windows, Linux, Mac OSX",
    python_requires=">=3.6",
    setup_requires=[
        'setuptools>=42.0',
        'wheel>=0.36.2'
    ],
    license='BSD-3-Clause',
    packages=['libusbsio'],
    package_data={
        'libusbsio': ['bin/*'],
    },
    include_package_data=True,
    author='Michal Hanak',
    author_email='michal.hanak@nxp.com',
    keywords=['LIBUSBSIO', 'USBSIO', 'SPI', 'I2C', 'GPIO'],
    #url='https://github.com/nxpmicro/libusbsio',
    #download_url='https://pypi.org/project/libusbsio/',
    project_urls={
        "NXP LIBUSBSIO Home": "https://www.nxp.com/design/software/development-software/library-for-windows-macos-and-ubuntu-linux:LIBUSBSIO",
        "MCULink Pro": "https://www.nxp.com/design/microcontrollers-developer-resources/mcu-link-pro-debug-probe:MCU-LINK-PRO",
        "LPCLink2": "https://www.nxp.com/design/microcontrollers-developer-resources/lpc-microcontroller-utilities/lpc-link2:OM13054",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Hardware',
        'Topic :: Utilities'
    ]
)

setup(**setup_args)

