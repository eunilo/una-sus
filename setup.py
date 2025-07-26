from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="unsa-sus-scraper",
    version="1.0.0",
    author="Eunilo",
    author_email="",
    description="Web scraper para coletar dados de cursos e ofertas da UNA-SUS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eunilo/unsa-sus",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "unsa-sus-scraper=scraper_unasus_incremental:main",
        ],
    },
    keywords="scraper, web-scraping, unasus, health, education, deia, diversity, equity, inclusion",
    project_urls={
        "Bug Reports": "https://github.com/eunilo/unsa-sus/issues",
        "Source": "https://github.com/eunilo/unsa-sus",
        "Documentation": "https://github.com/eunilo/unsa-sus#readme",
    },
) 