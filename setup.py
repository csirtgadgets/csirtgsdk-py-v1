from setuptools import setup

import dm.sdk
setup(
      name="dm-sdk",
      version=dm.sdk.__version__,
      description="DM Python SDK",
      long_description="DM Software Development Kit for Python",
      url="https://github.com/csirtgadgets/py-dm-sdk",
      license='LGPL3',
      classifiers=[
                   "Topic :: System :: Networking",
                   "Environment :: Other Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
                   "Programming Language :: Python",
                   ],
      keywords=['security'],
      author="Wes Young",
      author_email="wes@barely3am.com",
      packages = ["dm","dm.sdk","test"],
      install_requires = ["requests>=2.0"
                          "json",
                          'pyyaml',
                          'prettytable'],
      scripts=['bin/dm'],
      test_suite = "test"
)
