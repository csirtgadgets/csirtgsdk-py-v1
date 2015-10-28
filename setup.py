from setuptools import setup, find_packages

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'whitefacesdk/_version.py'
versioneer.versionfile_build = 'whitefacesdk/_version.py'
versioneer.tag_prefix = ''  # tags are like 1.2.0
versioneer.parentdir_prefix = 'py-whitefacesdk-'  # dirname like 'myproject-1.2.0'

setup(
    name="whitefacesdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="WhiteFace Python SDK",
    long_description="WhiteFace Software Development Kit for Python",
    url="https://github.com/csirtgadgets/py-whitefacesdk",
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
    author_email="wes@csirtgadgets.com",
    packages=find_packages(),
    install_requires=reqs,
    entry_points={
        'console_scripts': [
            "wf=whitefacesdk.client:main",
        ]
    },
    test_suite="test"
)
