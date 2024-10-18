from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="FoxLabel",  # tên của gói thư viện
    version="1.3",
    description="Thư viện hữu ích của Tuấn Anh.",
    url="https://pypi.org/project/FoxLabel/",
    author="Tuấn Anh - Foxconn",
    author_email="nt.anh.fai@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["lxml", "opencv-python", "ruamel.yaml", "pyyaml", "ntanh"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "FoxLabel=FoxLabel:start_program",
            "ntanh_foxlabel=FoxLabel:start_program",
        ],
    },
)
