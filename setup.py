#!/usr/bin/env python3
"""
Setup script for Amazon Review Scraper API
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="amazon-review-scraper-api",
    version="1.0.0",
    author="Amazon Review Scraper Team",
    author_email="your-email@example.com",
    description="A clean, easy-to-integrate API for scraping Amazon product reviews",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/amazon-review-scraper-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "amazon-review-scraper=amazon_review_api:main",
        ],
    },
    keywords="amazon, scraper, reviews, api, web-scraping, playwright, e-commerce",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/amazon-review-scraper-api/issues",
        "Source": "https://github.com/yourusername/amazon-review-scraper-api",
        "Documentation": "https://github.com/yourusername/amazon-review-scraper-api#readme",
    },
)
