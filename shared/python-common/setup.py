"""
Little Monster Common Library
Setup configuration for shared utilities across microservices
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lm-common",
    version="1.0.0",
    author="Little Monster Team",
    author_email="dev@littlemonster.dev",
    description="Shared utilities for Little Monster microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rogermmurphy/lm-1.0",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PyJWT>=2.8.0",
        "bcrypt>=4.1.0",
        "sqlalchemy>=2.0.23",
        "psycopg2-binary>=2.9.9",
        "redis>=5.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
    },
)
