import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name='PSLTDSim',
    version='0.0.1',
    description='Power System Long-Term Dynamic Simulation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/thadhaines/PSLTDSim',
    author='Thad Haines',
    author_email='jhaines@mtech.edu',
    license='MIT',
    packages=setuptools.find_packages(),
    zip_safe=False)
