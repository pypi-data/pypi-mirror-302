from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tquota",  # Name of the package
    version="0.0.3",  # Version number
    author="Abdussalam Aljbri",  # Author name
    author_email="mr.aljbri@gmail.com",  # Author email
    description="A processing timer module for cloud servers with session quota limitations.",
    long_description=long_description,  # Use the README.md as the long description
    long_description_content_type="text/markdown",  # Make sure to specify that it's markdown
    url="https://github.com/aljbri/tquota",  # Project GitHub URL
    packages=find_packages(),  # Automatically discover all the packages in your project
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3",  # Allows for all 3.x versions
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",  # OS compatibility
    ],
    python_requires='>=2.7, <4',  # Minimum version of Python required
    install_requires=[],  # Add any dependencies your package needs here
    keywords="quota timer cloud session limit processing kaggle colab",  # Useful keywords
    project_urls={
        "Bug Tracker": "https://github.com/aljbri/tquota/issues",  # URL to submit issues
        "Documentation": "https://github.com/aljbri/tquota/blob/main/README.md",  # Documentation URL
        "Source Code": "https://github.com/aljbri/tquota",  # Source code URL
    },
)
