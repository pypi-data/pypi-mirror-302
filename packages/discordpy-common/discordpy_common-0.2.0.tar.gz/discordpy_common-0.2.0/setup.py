from setuptools import setup, find_packages

setup(
    name='discordpy-common',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'discord.py',
        'motor',
        'pymongo',
    ],
    python_requires='>=3.12',
    author='pyPoul',
    license='MIT',
    description='Common tools for discord.py bots',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pyPoul/discordpy-common',
)
