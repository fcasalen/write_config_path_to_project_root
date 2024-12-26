from setuptools import setup, find_packages

setup(
    name='write_config_path_to_project_root',
    version='0.1.0',
    license="GNU General Public License",
    author="fcasalen",
    author_email="fcasalen@gmail.com",
    description="write configuration path to a project root so it can be used by the project",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 5 - Prodution/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12"
    ]
)
