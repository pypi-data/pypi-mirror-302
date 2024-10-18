import setuptools
setuptools.setup(
    name="deco_mllm",
    version="1.0.1",
    author="wcx",
    url='https://github.com/zjunlp/DeCo',
    author_email="2015248488@qq.com",
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=['tokenizers==0.13.3',
                      'huggingface-hub==0.25.0',
                      'accelerate==0.34.2',
                      'torch==2.4.1',
                      'torchvision==0.19.1']
)