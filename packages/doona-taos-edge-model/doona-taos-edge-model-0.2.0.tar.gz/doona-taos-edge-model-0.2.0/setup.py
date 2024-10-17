from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="doona-taos-edge-model",
    version="0.2.0",
    author="이운용",
    author_email="oncloudbros@gmail.com",
    description="TAOS Edge Model 예측 패키지",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages() + ['doona_taos_edge_model.schema'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements
)