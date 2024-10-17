from setuptools import setup

setup(
    name='geobuffers',
    version='0.1',
    description='geobuffers',
    long_description='geobuffers mini package for calculating geodetic areas around points',
    author='Mikolaj Czerkawski',
    author_email="mczerkawski96@gmail.com",
    package_dir={"geobuffers":"src"},
    install_requires=["shapely","pyproj"]
)
