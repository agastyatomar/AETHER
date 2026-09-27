#!/usr/bin/env python3
"""Setup script for AETHER - backwards compatibility for pip install."""

from setuptools import setup, find_packages

setup(
    name="aether",
    version="0.1.0",
    description="AETHER — voice-driven meta-orchestrator that turns one spoken request into a fleet of self-checking AI agents",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Aadi Tomar",
    author_email="agastyatomar@example.com",
    url="https://github.com/agastyatomar/AETHER",
    packages=find_packages(include=["aether*"]),
    python_requires=">=3.11",
    install_requires=[
        "pydantic>=2.8.0",
        "aiosqlite>=0.20.0",
        "filelock>=3.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=5.0.0",
            "ruff>=0.5.0",
            "mypy>=1.10.0",
            "watchdog>=4.0.0",
        ],
        "docs": [
            "watchdog>=4.0.0",
        ],
        "browser": [
            "browser-use>=0.13.10",
            "playwright>=1.62.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aether = aether.cli:main",
            "aether-browser-install = aether.society.browser.install:main",
            "aether-society = aether.society.runtime:main",
            "aether-gui-install = aether.gui_install:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords=["ai", "agents", "orchestration", "voice", "automation", "browser-automation"],
    project_urls={
        "Homepage": "https://github.com/agastyatomar/AETHER",
        "Repository": "https://github.com/agastyatomar/AETHER",
        "Issues": "https://github.com/agastyatomar/AETHER/issues",
        "Documentation": "https://github.com/agastyatomar/AETHER/wiki",
    },
)