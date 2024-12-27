from setuptools import setup, find_packages

setup(
    name="ai-customer-service",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.2",
        "torch>=1.9.0",
        "redis>=4.5.1",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.9.0",
    ],
    author="Bharath Janumpally",
    author_email="bharathreddy.janumpally@gmail.com",
    description="AI-Driven Multi-Channel Customer Service Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-customer-service",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
