from setuptools import setup, find_packages

setup(
    name="StreamAudio",  # Updated package name
    version="0.1.0",  # Initial version
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for real-time audio streaming in memory for flexible use cases",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/streamaudio",  # Replace with your repository URL
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        "pyaudio",  # Dependency for audio capture
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Specify supported Python versions
)
