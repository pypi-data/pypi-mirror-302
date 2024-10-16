from setuptools import setup, find_packages

setup(
    name='AgentMix',
    version='1.6',
    packages=find_packages(),
    install_requires=[
        'httpx',
    'asyncio',
    'colorama',
    'beautifulsoup4',# List any dependencies here, e.g., 'numpy', 'pandas'
    ],
    entry_points={
        'console_scripts': [
            'agentmix=AgentMix.main:main',  # Adjust 'main' if your entry function is different
        ],
    },
)
