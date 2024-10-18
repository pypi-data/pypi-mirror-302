from setuptools import setup, find_packages

setup(
    name="browseek",
    version="0.1.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add any dependencies here
    ],
    author="Tom Sapletta",
    author_email="info@softreck.dev",
    description="Advanced multi-browser automation library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.browseek.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
