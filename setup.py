import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name="fipradioPlaylist",
      version="0.1.0",
      author="jcoin",
      author_email="jrlamoule@gmail.com",
      long_description=README,
      long_description_content_type="text/markdown",
      description="Library to access the previous, current and future tracks "
                  "from FIP Radio & its webradio",
      url="https://github.com/jcoin/fipradio-playlist",
      license="MIT",
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: MIT License",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3 :: Only"],
      install_requires=['requests'],
      packages=["fipradioPlaylist"],
      py_modules=['fipplaylistClient'],
      scripts=[])
