from setuptools import setup, find_packages
import os
# 从VERSION文件中获取版本号
VERSION = open(os.path.join(os.path.dirname(__file__), 'VERSION')).read().strip()
setup(
    name="dagent_llm",
    packages=find_packages(),
    install_requires=[
        # 依赖包，例如 click, requests 等
        "dsqlenv",
        "langchain_core",
        "langchain_openai",
    ],
    author="Zhao Sheng",
    author_email="zhaosheng@nuaa.edu.cn",
    description="A package for LLM operations.",
    version=VERSION,
    entry_points={
        'console_scripts': [
            # dagent_llm.cli.main
            'dagent_llm=dagent_llm.cli:main',
        ],
    },
)
