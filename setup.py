from setuptools import setup, find_packages
import os

# Read README file
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip() and not line.startswith('#')]

setup(
    name="project-evee",
    version="1.0.0",
    author="Project Evee Team",
    description="Voice-Controlled Automation Assistant",
    long_description="Project Evee is a voice-controlled automation assistant that records voice commands, transcribes them using AI, and generates automation code to perform tasks on your computer.",
    long_description_content_type="text/plain",
    url="https://github.com/yourusername/project-evee",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        "Topic :: Office/Business :: Office Suites",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "project-evee=main_gui:main",
        ],
        "gui_scripts": [
            "project-evee-gui=main_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json"],
    },
    data_files=[
        ("", ["requirements.txt"]),
    ],
    keywords="voice automation assistant AI transcription",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/project-evee/issues",
        "Source": "https://github.com/yourusername/project-evee",
        "Documentation": "https://github.com/yourusername/project-evee/wiki",
    },
) 