from setuptools import setup, find_packages

setup(
    name="graphs_yujin_k9",
    version="1.1.3",
    packages=find_packages(),
    include_package_data=True, 
    package_data={
        '': ['*.py'],  
    },
    install_requires=[],
)
