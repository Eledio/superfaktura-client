from setuptools import setup, find_namespace_packages

setup(
    name="superfaktura_client",
    version="1.0.0",
    packages=find_namespace_packages(),
    url="https://github.com/eledio-helpers/superfaktura-client",
    license="MIT",
    author="Richard Kubíček",
    author_email="kubicekr@eledio.com",
    install_requires=["requests", "python-dotenv"],
)
