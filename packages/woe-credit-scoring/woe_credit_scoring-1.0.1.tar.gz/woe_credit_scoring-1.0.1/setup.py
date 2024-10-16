from setuptools import setup, find_packages

setup(
    name="woe-credit-scoring",
    version="1.0.1",  
    author="José G. Fuentes, PhD",
    author_email="jose.gustavo.fuentes@gmail.com",
    description="Tools for creating credit scoring models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JGFuentesC/woe_credit_scoring",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    install_requires=[
        # Lista de dependencias del paquete
        "numpy>=2.1.2",
        "pandas>=2.2.3",
        "scikit-learn>=1.5.2",
        "seaborn>=0.13.2",
        "matplotlib>=3.9.2"
    ]
)
