from setuptools import setup, find_packages

setup(
    name="cloey-orm",
    version="0.0.2",
    description="cloey orm is a simple ORM for Fastapi, flask and other python framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jose Machava",
    author_email="jose.machava@xindiri.com",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)