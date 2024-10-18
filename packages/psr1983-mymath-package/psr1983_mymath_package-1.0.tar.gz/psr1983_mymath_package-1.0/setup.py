from setuptools import setup, find_packages

VERSION = '1.0' 
DESCRIPTION = 'My Math Python Package'
LONG_DESCRIPTION = 'My Math Python Package for add/subtract/multiply/divide'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="psr1983_mymath_package", 
        version=VERSION,
        author="Shunmuga",
        author_email="psr@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'math'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)