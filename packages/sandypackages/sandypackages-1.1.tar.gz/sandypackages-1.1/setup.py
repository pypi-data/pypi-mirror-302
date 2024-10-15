from setuptools import setup, find_packages

setup(
    name='sandypackages',                     # Package name
    version='1.1',                       # Version of your package
    description='Data_Analyst_PKG',# Short description of the package
    long_description=open('README.md').read(),  # Optional: Readme file
    long_description_content_type='text/markdown', # Optional: Specify markdown format
    author='vishwanath',                    # Author name
    author_email='vishwa64@outlook.com', # Author email
    #url='https://github.com/yourusername/my_package',  # URL to the package homepage
    license='MIT',                         # License type
    packages=find_packages(),              # Automatically find package subdirectories
    install_requires=[                     # List of dependencies (optional)
        # 'requests',
    ],
    classifiers=[                          # Additional metadata about the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',               # Minimum Python version required
)
