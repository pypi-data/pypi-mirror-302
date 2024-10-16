from setuptools import setup, find_packages

setup(
    name="hello-world-brianckwu",  # Name of the package
    version="0.1",  # Initial release version
    description="A simple hello world package",
    author="Cheng-Kuang (Brian) Wu",
    author_email="brianckwu@gmail.com",
    packages=find_packages(),  # Automatically find packages in the current directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # Specify minimum Python version
)
