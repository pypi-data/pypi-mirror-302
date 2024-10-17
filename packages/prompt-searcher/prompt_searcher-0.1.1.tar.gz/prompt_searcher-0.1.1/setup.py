from setuptools import setup, find_packages

setup(
    name="prompt_searcher",
    version="0.1.1",
    description=(
        "PromptSearcher is an automatic tool designed to find the best prompt in both "
        "supervised and unsupervised scenarios. This project draws inspiration from traditional "
        "neural network learning techniques."
    ),
    author="octaviopavon",
    author_email="octavio.pavon@botman-ai.com",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/octaviusp/PromptSearcher",  # Update with actual repo URL
    packages=find_packages(include=["prompt_searcher", "prompt_searcher.*"]),  # Include all sub-packages
    install_requires=[
        "openai>=1.51.2,<2.0.0",
        "polars>=1.9.0,<2.0.0",
        "numpy>=2.1.2,<3.0.0",
        "python-dotenv>=1.0.1,<2.0.0",
        "anthropic>=0.36.1,<1.0.0",
        "groq>=0.11.0,<1.0.0",
        "matplotlib>=3.9.2,<4.0.0",
    ],
    python_requires=">=3.12",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3,<8.0.0",
            "python-dotenv>=1.0.0,<2.0.0",
        ]
    },
)