import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name='PSLTDSim',
    version='0.1.0',
    author="Thad Haines",
    author_email="jhaines@mtech.edu",
    description='Power System Long-Term Dynamic Simulator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/thadhaines/PSLTDSim',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )
