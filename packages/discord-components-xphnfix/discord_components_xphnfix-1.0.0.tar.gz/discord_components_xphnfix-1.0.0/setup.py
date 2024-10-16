from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Fork and Fix of/for discord_components, an unofficial library for discord components.'
LONG_DESCRIPTION = 'Original Author: kiki7000 (devkiki7000@gmail.com). I fixed some errors (requirements errors) and am adding some more things to it.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="discord_components_xphnfix", 
        version=VERSION,
        author="Xylen",
        author_email="priyanshudeb3@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license="MIT License",
        url="https://debxylen.github.io/discord_components/",
        packages=["discord_components", "discord_components.ext"],
        install_requires=["discord.py", "aiohttp"],
        python_requires=">=3.6",
        keywords=['python', 'discord', 'discord.py', 'discord-components'],
        classifiers= [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        ]
)
