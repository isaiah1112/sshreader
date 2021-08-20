#!/usr/bin/env python2
# coding=utf-8
"""Setup file for sshreader module"""

from setuptools import setup


setup(name='sshreader',
      version='4.7',
      description='Multi-threading/processing wrapper for Paramiko',
      author='Jesse Almanrode',
      author_email='jesse@almanrode.com',
      url='http://sshreader.readthedocs.io/',
      project_urls={'Documentation': 'http://sshreader.readthedocs.io/',
                    'Source': 'https://bitbucket.org/isaiah1112/sshreader/',
                    'Tracker': 'https://bitbucket.org/isaiah1112/sshreader/issues'},
      packages=['sshreader'],
      include_package_data=True,
      scripts=['bin/pydsh'],
      install_requires=['click>=8.0.1',
                        'colorama>=0.4.4',
                        'paramiko>=2.7.2',
                        'progressbar2>=3.53.1',
                        'python-hostlist>=1.21',
                        ],
      platforms=['Linux', 'Darwin'],
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      )
