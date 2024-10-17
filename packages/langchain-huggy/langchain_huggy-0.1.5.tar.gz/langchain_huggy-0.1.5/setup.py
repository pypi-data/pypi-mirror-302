from setuptools import setup, find_packages

setup(
    name="langchain_huggy",
    version="0.1.5",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "langchain",
        "hugchat",
        "python-dotenv",
    ],
    extras_require={
        "dev": ["pytest", "black", "isort"],
    },
)