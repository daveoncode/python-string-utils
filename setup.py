import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='python-string-utils',
    version='1.0.0',
    description='Utility functions for strings validation and manipulation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Davide Zanotti',
    author_email='davidezanotti@gmail.com',
    license='MIT',
    url='https://github.com/daveoncode/python-string-utils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='string str utilities validation compression development',
    packages=['string_utils'],
    data_files=[('README', ['README.md'])],
    python_requires='>=3.5',
    setup_requires=['wheel'],
)
