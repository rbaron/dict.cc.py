from setuptools import setup, find_packages

setup(
      name="dict.cc.py",
      description="Unofficial dict.cc command line interface",
      version="3.0.0",
      url="https://github.com/rbaron/dict.cc.py",
      install_requires=["beautifulsoup4","requests"],
      packages=find_packages(),
      scripts=["scripts/dict.cc.py"]
     )
