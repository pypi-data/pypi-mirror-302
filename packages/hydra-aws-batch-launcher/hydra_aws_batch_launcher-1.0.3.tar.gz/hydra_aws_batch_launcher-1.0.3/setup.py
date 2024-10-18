from pathlib import Path

from read_version import read_version
from setuptools import find_namespace_packages, setup

setup(
    name="hydra-aws-batch-launcher",
    version=read_version("hydra_plugins/hydra_aws_batch_launcher", "__init__.py"),
    author="philkohl",
    author_email="65112414+philkohl@users.noreply.github.com",
    description="AWS Batcher Launcher for Hydra apps",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/philkohl/hydra_aws_batch_launcher/",
    packages=find_namespace_packages(include=["hydra_plugins.*"]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "hydra-core>=1.3.2",
    ],
    include_package_data=True,
)
