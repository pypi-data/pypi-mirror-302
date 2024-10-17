from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name='geoscan_arena_sdk',
  include_package_data=True,
  version='1.0',
  license='MIT',
  description='Programming tools for programming Geoscan arena robots',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Geoscan',
  author_email='info@geoscan.aero',
  install_requires=[
          'pymavlink==2.4.37',
          'pyserial==3.5',
          'future==0.18.3',
          'requests',
      ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.9',
)