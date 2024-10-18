from setuptools import setup, find_packages

with open("README.md", "r") as desc_file:
    long_description = desc_file.read()

setup(
    name="PyWLGK",
    version="1.0.1",
    description="Python package computing Weisfeiler-Lehman graph kernels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author="Roman Joeres",
    maintainer="Roman Joeres",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[],
    package_data={},
    python_requires=">=3.8, <4.0.0",
    keywords="bioinformatics, computer-science, graph-kernels, machine-learning, python, wlgk, weisfeiler-lehman-graph-kernel",
)
