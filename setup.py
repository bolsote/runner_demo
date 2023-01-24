from setuptools import find_packages, setup

setup(
    name="runner_demo",
    version="23.1.0",
    author="Víctor Muñoz",
    author_email="victorm@marshland.es",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "attrs>=20.2",
        "zope.interface>=5.0",
        "mypy-zope>=0.3.3",
    ],
    extras_require={
        "dev": [
            "bandit",
            "bumpver>=2021.1109",
            "black>=22.1",
            "coverage[toml]>=5.0",
            "flake8",
            "flake8-bugbear",
            "hypothesis>=6.0",
            "isort>=5.0",
            "mypy>=0.920",
            "pdbpp",
            "pip-audit",
            "pylint",
            "pytest>=6.0",
            "pytest-cov>=3.0",
            "tox",
        ],
    },
    python_requires=">=3.9",
    zip_safe=False,
)
