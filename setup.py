from setuptools import setup, find_packages

setup(
    name="vrel",
    version="0.1.0",
    description="A Natural Language Understanding and Execution library",
    author="",
    author_email="",
    license="MIT",
    python_requires=">=3.10",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
        ],
    },
)