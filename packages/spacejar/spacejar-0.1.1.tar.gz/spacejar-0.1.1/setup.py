import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from spacejar.installer import install_binary

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        print("Running PostInstallCommand after pip install...")
        install.run(self)  # Run the standard install command
        install_binary()   # Call the custom binary installation function

setup(
    name="spacejar",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "platformdirs"
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'spacejar_cli=spacejar.cli:main', # renamed to avoid conflicts with Rust binary
        ],
    },
    author="Spacejar Team",
    author_email="engineers@spacejar.io",
    description="Installs the Spacejar CLI (Rust binary)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/spacejar-labs/spacejar-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
