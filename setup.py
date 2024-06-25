from setuptools import find_packages, setup

setup(
    name="Aligner-SUPERB",
    version="0.1.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": []},
    description="Aligner-SUPERB",
    author="lifeiteng0422@gmail.com",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    python_requires=">=3.8",
    install_requires=[
        "pre-commit==3.6.0",
        "lhotse",
        "praatio",
    ],
    entry_points={
        "console_scripts": [
            "alignersuperb=alignersuperb.bin:run"
        ],
    },
    include_package_data=True,
)
