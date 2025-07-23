import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unihiker",
    version="0.0.28.5",
    author="unihiker Team",
    author_email="unihiker@dfrobot.com",
    description="Library for Unihiker M10",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UNIHIKER/unihiker-pypi-lib",
    project_urls={
        "Bug Tracker": "https://github.com/UNIHIKER/unihiker-pypi-lib",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={
        "": ["*.ttf", "*.otf", "emojis/*"],
    },
    install_requires=['fontTools', 
                        'pillow', 
                        'qrcode', 
                        'pydub', 
                        'pygame',
                        'pyaudio; platform_system=="Windows"',
                        'pyaudio; platform_system=="Linux"'],
    python_requires=">=3.6",
)