from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class CustomInstallCommand(install):
    """Custom command to run `playwright install` after package installation."""
    def run(self):
        # Run the standard install
        install.run(self)
        # Automatically run `playwright install` to install the browser binaries
        try:
            subprocess.check_call(["playwright", "install"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Playwright browsers: {str(e)}")


setup(
    name="vestapy",  # Replace with your desired package name
    version="0.1.0",  # Initial version, update as needed
    author="Virgil Vaduva",  # Replace with your name
    author_email="vvaduva@gmail.com",  # Replace with your email
    description="A Python project for interacting with the Vestaboard local API and post content from various integrations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/booyasatoshi/vestaboard",  # Replace with your GitHub URL
    packages=find_packages(include=["vestaboard", "vestaboard.*"]),  # Include all submodules
    install_requires=[
        "requests",
        "python-dotenv",
        "playwright",  # Ensure Playwright is installed
    ],
    package_data={
        'vestaboard': ['data/*.json', '.env.sample'],  # Include JSON files in the package
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify Python version compatibility
    cmdclass={
        'install': CustomInstallCommand,  # Use the custom install command to run Playwright installation
    },
)
