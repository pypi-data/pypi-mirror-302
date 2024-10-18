import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apccapi",
    version="0.0.1",
    author="APEC Climate Center",
    author_email="joohyung@apcc21.org",
    description="APCC Climate Information toolKit API package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.apcc21.org",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords=[
        'APCC', 'apcc', 'Climate', 'Climate Information', 'Climate API'
    ],
    install_requires=[
        'requests',
        'urllib3',
    ],
    project_urls={
        "CLIK": "https://cliks.apcc21.org",
    },
)