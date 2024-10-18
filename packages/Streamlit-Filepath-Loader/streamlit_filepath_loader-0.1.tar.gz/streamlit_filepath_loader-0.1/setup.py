from setuptools import setup, find_packages
with open ("README.md", "r") as f:
    description = f.read()
setup(
    name='Streamlit-Filepath-Loader',
    version='0.1',
    packages=find_packages(),
    install_requires=['streamlit==1.39.0'],
    long_description=description,
    long_description_content_type="text/markdown",
)
# Add dependencies here.
# e.g. 'numpy>=1.11.1'
