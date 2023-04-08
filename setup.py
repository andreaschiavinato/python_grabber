from pathlib import Path
from setuptools import setup

setup(name='pygrabber',
      version='0.1',
      description='Module for grabbing live video images using DirectShow',
      long_description=(Path(__file__).parent / "README.md").read_text(),
      long_description_content_type='text/markdown'
      url='https://github.com/andreaschiavinato/python_grabber',
      author='andreaschiavinato',
      author_email='',
      license='MIT',
      packages=['pygrabber'],
      package_data={"pygrabber": ["py.typed"]},
      install_requires=[
          "comtypes>=1.1.7",
          "numpy>=1.17.3"
      ],
      zip_safe=False)
