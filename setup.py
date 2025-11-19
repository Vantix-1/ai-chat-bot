"""
Setup script for AI Chat Bot project
"""
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ai-chat-bot",
    version="1.0.0",
    description="AI-powered chat bot with OpenAI integration",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.11",
    author="Vance Frommer",
    author_email="vance@futurename",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)