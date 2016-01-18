from setuptools import setup, find_packages

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'csirtgsdk/_version.py'
versioneer.versionfile_build = 'csirtgsdk/_version.py'
versioneer.tag_prefix = ''  # tags are like 1.2.0
versioneer.parentdir_prefix = 'py-csirtgsdk-'  # dirname like 'myproject-1.2.0'

setup(
    name="csirtgsdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CSIRTG Python SDK",
    long_description="CSIRTG Software Development Kit for Python",
    url="https://github.com/csirtgadgets/py-csirtgsdk",
    license='LGPL3',
    classifiers=[
        "Topic :: System :: Networking",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python"
    ],
    keywords=['security'],
    author="Wes Young",
    author_email="wes@csirtgadgets.org",
    packages=find_packages(),
    install_requires=reqs,
    entry_points={
        'console_scripts': [
            "csirtg=csirtgsdk.client:main",
        ]
    },
    test_suite="test"
)
