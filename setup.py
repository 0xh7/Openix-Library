from setuptools import setup, find_packages

setup(
    name="Openix",
    version="2.0.2",  
    description="A simple chess openings (ECO) library for Python.",
    author="0xh7",
    author_email="fjdjfjd1424@gmail.com",
    packages=find_packages(),
    install_requires=[
        "python-chess",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        "Openix": ["open/*.json"],
    },
    url="https://github.com/0xh7/Openix-Library",
     keywords=[
        "chess", "ECO", "openings", "chess openings",
        "ai chess", "python chess", "openix", "game opening",
        "board games", "chess library", "python library",
        "python chess library", "python chess openings",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
