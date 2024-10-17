import os
from setuptools import setup, find_packages
from pathlib import Path

# Set the package name for the CUDA version
package_name = "celux-cuda"
version = "0.2.7"   # Version for CUDA version

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")


setup(
    name=package_name,  # Package name on PyPI will be "celux-cuda"
    version=version,
    author="Trenton Flanagan",
    author_email="spigonvids@gmail.com",
    description="HW accelerated video reading for ML Inference (CUDA version).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Trentonom0r3/celux",  # Update with the correct GitHub URL
    packages=find_packages(where="celux_cuda"),  # Packages from celux_cuda/ directory
    package_dir={"": "celux_cuda"},  # Install as celux module
    package_data={
        "celux": ["*.pyd", "*.dll", "*.pyi", "*.py"],  # Include CUDA-specific binaries
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: Microsoft :: Windows",
    ],
    license="AGPL-3.0",
    python_requires=">=3.11",
    include_package_data=True,
    zip_safe=False,
)
