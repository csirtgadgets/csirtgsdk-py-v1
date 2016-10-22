from setuptools import setup, find_packages
import os
import sys
import versioneer

with open('requirements.txt') as f:
    reqs = f.read().splitlines()


# https://www.pydanny.com/python-dot-py-tricks.html
if sys.argv[-1] == 'test':
    test_requirements = [
        'pytest',
        'coverage',
        'pytest_cov',
    ]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        err_msg = e.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirments." % err_msg
        raise ImportError(msg)
    r = os.system('py.test test -v --cov=csirtgsdk --cov-fail-under=25')
    if r == 0:
        sys.exit()
    else:
        raise RuntimeError('tests failed')

setup(
    name="csirtgsdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CSIRTG Python SDK",
    long_description="CSIRTG Software Development Kit for Python",
    url="https://github.com/csirtgadgets/csirtgsdk-py",
    license='LGPL3',
    classifiers=[
        "Topic :: System :: Networking",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python"
    ],
    keywords=['network','security'],
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
