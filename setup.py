"""Macro module for Gimmebio.
Based on: https://blog.shazam.com/python-microlibs-5be9461ad979
"""


import os
from six import iteritems
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

PACKAGE_NAME = 'gimmebio'


SOURCES = {
    'gimmebio.seqs': 'gimmebio/seqs',
    'gimmebio.kmers': 'gimmebio/kmers',
    'gimmebio.linked_reads': 'gimmebio/linked_reads',
    'gimmebio.ram_seq': 'gimmebio/ram_seq',
    'gimmebio.text_plots': 'gimmebio/text_plots',
}


def install_microlibs(sources, develop=False):
    """ Use pip to install all microlibraries.  """
    print('Installing all microlibs in {} mode'.format(
              'development' if develop else 'normal'))
    working_dir = os.getcwd()
    for name, path in iteritems(sources):
        try:
            os.chdir(os.path.join(working_dir, path))
            if develop:
                check_call(["python", '-m', 'pip', 'install', '-e', '.'])
            else:
                check_call(["python", '-m', 'pip', 'install', '.'])
        except Exception as e:
            print('Something went wrong installing', name)
            print(e)
        finally:
            os.chdir(working_dir)


class DevelopCmd(develop):
    """ Add custom steps for the develop command """
    def run(self):
        install_microlibs(SOURCES, develop=True)
        develop.run(self)


class InstallCmd(install):
    """ Add custom steps for the install command """
    def run(self):
        install_microlibs(SOURCES, develop=False)
        install.run(self)


setup(
    name=PACKAGE_NAME,
    version='0.3.0',
    author='David Danko',
    author_email='dcdanko@gmail.com',
    description='Utilities and explorations in computational biology',
    license='MIT License',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'future',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'gimmebio=gimmebio.cli:main'
        ]
    },
    cmdclass={
        'install': InstallCmd,
        'develop': DevelopCmd,
    },
    packages=[PACKAGE_NAME],
    package_dir={PACKAGE_NAME: 'gimmebio'},
)
