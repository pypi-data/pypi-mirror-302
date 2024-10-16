from setuptools import setup, find_packages # type: ignore

# Read the contents of README.md as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tokenizer-figma",  # Module name
    version="1.0.4",
    author="Byron",
    author_email="byronforrestwhite@outlook.com",
    description="A Python package for generating and managing design tokens for Figma, with Material Theme Builder integration and Tokens Studio plugin support.",  # Short description
    long_description=long_description,  # Detailed description from README.md
    long_description_content_type="text/markdown",  # Content type of long description
    url="https://github.com/ByronFW/style-tokenizer-figma",
    packages=find_packages(),  # Automatically finds all packages
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Minimum required Python version
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
)