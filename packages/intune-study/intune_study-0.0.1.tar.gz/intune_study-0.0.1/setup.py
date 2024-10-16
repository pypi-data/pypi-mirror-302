from setuptools import setup, find_packages

setup(
    name='intune_study',  # Name of your package
    version='0.0.1',  # Initial version of your package
    description='A Python package for managing device compliance policies in Intune using Microsoft Graph API',
    author='Shiyas Shaji',  # Replace with your name
    author_email='shiyasshaji1999@gmail.com',  # Replace with your email
    packages=find_packages(),  # Automatically find all packages
    install_requires=[  # List of dependencies your package needs
        'requests',
        'python-dotenv',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
