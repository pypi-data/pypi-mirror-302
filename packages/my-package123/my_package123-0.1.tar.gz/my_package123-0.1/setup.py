from setuptools import setup, find_packages

setup(
    name='my_package123',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='',
    author_email='',
    description='A simple utility package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
