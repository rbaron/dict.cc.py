from setuptools import setup, find_packages

setup(
      name="dict.cc.py",
      description="Unofficial dict.cc command line interface",
      version="2.0",
      url="http://github.com/rbaron/dict.cc.py",
      install_requires=["beautifulsoup4"],
      packages=find_packages(),
      scripts=["scripts/dict.cc.py"]
     )
