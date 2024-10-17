from setuptools import setup, find_packages

setup(
    name="memnoch_utils",
    version="0.1.4",
    author="Guillaume LEFEBVRE",
    author_email="guillaume@ldmail.fr",
    description="",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Memnoch9178/mem-utils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    include_package_data=True,
)
