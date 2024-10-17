import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name="pyctype",
  version="7.4.0",
  author="tanket",
  author_email="tanket@assurmail.net",
  description="Interact with cython, python, ctypes, and use other c/c++ tools",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/notepads/ctype",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ]
)
