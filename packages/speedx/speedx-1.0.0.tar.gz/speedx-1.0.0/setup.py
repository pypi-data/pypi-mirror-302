from setuptools import setup, find_packages

setup(
    name='speedx',  # Package name
    version='1.0.0',  # Initial release version
    description='A simple network speed tester utility for the terminal.',  # Brief description
    long_description=open('README.md').read(),  # Read long description from README file
    long_description_content_type='text/markdown',  # Specify the format of the long description
    author='Abhinav',  # Your name
    author_email='upstage.barrier_0x@icloud.com',  # Your email
    packages=find_packages(),  # Automatically find packages in the current directory
    install_requires=[
        'click>=8.0',
        'matplotlib>=3.5',
        'termplotlib>=0.3.0',
        'colorama>=0.4.4',
        'requests>=2.26.0',
        'speedtest-cli',  # Ensure speedtest-cli is included as a dependency
    ],
    entry_points={
        'console_scripts': [
            'speedx=speedx.cli:cli',  # Entry point for command line interface
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',  # Development status
        'Environment :: Console',  # Environment type
        'Intended Audience :: Developers',  # Target audience
        'License :: OSI Approved :: MIT License',  # License information
        'Programming Language :: Python :: 3',  # Supported Python versions
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',  # OS compatibility
        'Topic :: Software Development :: Libraries :: Python Modules',  # Software topic
        'Topic :: Utilities',  # Utility tools
    ],
    python_requires='>=3.7',  # Python version requirement
    include_package_data=True,  # Include additional files specified in MANIFEST.in
)
