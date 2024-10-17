from setuptools import setup, find_packages

setup(
    name="langchain_huggy",
    version="0.2.2",  # Incremented the version number
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "langchain",
        "hugchat",
        "python-dotenv",
        "fastapi",
        "uvicorn",
        "click",  # Added for CLI functionality
    ],
    extras_require={
        "dev": ["pytest", "black", "isort"],
    },
    entry_points={
        'console_scripts': [
            'langchain_huggy=langchain_huggy.cli:cli',
        ],
    },
)