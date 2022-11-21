# coding=utf-8
"""Setup file for sshreader module"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='sshreader',
                 version='5.0.4',
                 author='Jesse Almanrode',
                 author_email='jesse@almanrode.com',
                 description='Multi-threading/processing wrapper for Paramiko',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='http://sshreader.readthedocs.io/',
                 project_urls={'Documentation': 'http://sshreader.readthedocs.io/',
                               'Source': 'https://bitbucket.org/isaiah1112/sshreader/',
                               'Tracker': 'https://bitbucket.org/isaiah1112/sshreader/issues'},
                 packages=['sshreader', 'sshreader/scripts'],
                 include_package_data=True,
                 python_requires='>=3.7',
                 install_requires=['click>=8.1.3',
                                   'colorama>=0.4.6',
                                   'paramiko>=2.12.0',
                                   'progressbar2>=4.2.0',
                                   'python-hostlist>=1.22',
                                   ],
                 entry_points={'console_scripts': ['pydsh = sshreader.scripts.pydsh:cli']},
                 platforms=['Linux', 'Darwin'],
                 classifiers=[
                     'Programming Language :: Python',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                     'Development Status :: 5 - Production/Stable',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: 3.9',
                     'Programming Language :: Python :: 3.10',
                     'Programming Language :: Python :: 3.11',
                     'Topic :: Software Development :: Libraries',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                 ],
                 )
