from setuptools import setup, find_packages

setup(
    name="graphs_yujin_k9",
    version="1.1.4",
    packages=find_packages(include=['graphs_yujin_k9', 'graphs_yujin_k9.*']),  
    include_package_data=True, 
    package_data={
        '': ['*.py'],  
    },
    install_requires=[],
)
