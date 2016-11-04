from distutils.core import setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='python-string-utils',
    version='0.5.0',
    description='Utility functions for strings checking and manipulation.',
    long_description=long_description,
    author='Davide Zanotti',
    author_email='davidezanotti@gmail.com',
    license='MIT',
    url='https://github.com/daveoncode/python-string-utils',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='string str utilities development',
    py_modules=['string_utils'],
    data_files=[('README', ['README.md'])],
)
