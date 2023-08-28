from setuptools import setup, find_packages

setup(
    name="roy-app",
    version="0.1.0",
    url="https://github.com/PypayaTech/roy-app",
    author="PypayaTech",
    description="A tool for annotating regions of interest (ROI) in images",
    readme="README.md",
    license="MIT",
    packages=find_packages(),
    install_requires=["Pillow"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "image-annotator = image_annotator.main:main",
        ],
    },
)
