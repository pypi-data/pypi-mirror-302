from setuptools import setup, find_packages

setup(
    name='example_package_hagikehappy',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # 列出你的依赖包
    ],
    include_package_data=True,
    package_data={
        'example_package_hagikehappy': [
        ],
    },
    description='A simple example Python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='hagikehappy',
    author_email='hagikehappy@163.com',
    python_requires='>=3.10',
    classifiers=[  
        "Programming Language :: Python :: 3",  
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",  
    ],  
    project_urls={  
        'Homepage': 'https://github.com/pypa/sampleproject',  
        'Issues': 'https://github.com/pypa/sampleproject/issues',  
    },  
)

