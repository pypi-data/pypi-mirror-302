from setuptools import setup, find_packages

setup(
    name="cometSrv",
    version="0.1",
    description="Comet Security Module that have features for server logging.",
    author="asdf.3643",  # Replace with your name
    packages=find_packages(),
    install_requires=[
        "disnake",  # Change to 'discord.py' if you're using that library
        "discord",
        "requests"  # Required for sending webhook requests
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Specify the license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # Minimum Python version
)
