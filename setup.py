from setuptools import setup

import whiteface.sdk
setup(
      name="whiteface-sdk",
      version=whiteface.sdk.VERSION,
      description="WhiteFace Python SDK",
      long_description="WhiteFace Software Development Kit for Python",
      url="https://github.com/csirtgadgets/py-whiteface-sdk",
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
      packages = ["whiteface","whiteface.sdk","test"],
      install_requires = ["requests>=2.0"
                          "json",
                          'pyyaml',
                          'prettytable'],
      scripts=['bin/wf'],
      test_suite = "test"
)
