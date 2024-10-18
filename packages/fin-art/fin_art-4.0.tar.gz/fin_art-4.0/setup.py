from setuptools import setup, find_packages

setup(
    name="fin_art",  
    version="4.0", 
    description="A module for generating stylistic images",
    author="madvasik",  
    author_email="ma2sic@yandex.ru",  
    packages=find_packages(), 
    python_requires=">=3.6",  
    install_requires=[  
        "torch",
        "transformers",
        "diffusers",
        "matplotlib",
        "peft"
    ],
)