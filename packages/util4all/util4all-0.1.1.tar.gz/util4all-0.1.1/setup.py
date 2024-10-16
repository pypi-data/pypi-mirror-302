from setuptools import setup, find_packages

def read_requirements():
    try:
        with open("./requirements.txt") as req_file:
            packages = req_file.read().splitlines()
            print(f"Packages: {packages}")
            return packages
    except FileNotFoundError:
        print("requirements.txt not found. No additional packages will be installed.")
        return []

setup(
    name="util4all",
    version="0.1.1",
    description="Common utility methods for enterprise projects",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Antoine Fusilier",
    author_email="antoinefusilier@gmail.com",
    url="https://github.com/CYBA7K2M-COMMON8Z/COMMON8Z_UTIL4ALL.git",  # Your repository
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            f"util4all = util4all.main:cli",  # CLI command setup
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=read_requirements(),
)
