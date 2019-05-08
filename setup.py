from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = list(map(str.strip, f))

setup(
    name='ZirkelWebsite',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
)
