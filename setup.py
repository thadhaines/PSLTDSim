import setuptools
import os

def read(fname):
    readPath = os.path.join(os.path.dirname(__file__), fname)
    print("reading: %s" % readPath)
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open("README.md", "r") as fh:
    long_description = fh.read()

#print(long_description)

setuptools.setup(
	name='PSLTDSim',
    version='0.0.2',
    description='Power System Long-Term Dynamic Simulation',
    #long_description=read('README.md'),
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url='https://github.com/thadhaines/PSLTDSim',
    author='Thad Haines',
    author_email='jhaines@mtech.edu',
    license='MIT',
    packages=setuptools.find_packages(),
    zip_safe=False)
