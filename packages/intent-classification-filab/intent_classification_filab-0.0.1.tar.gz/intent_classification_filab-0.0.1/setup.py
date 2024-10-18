from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="intent_classification_filab",
    version="0.0.1",
    author="jackaa",
    author_email="jackaa@filab.co.kr",
    description="사용자 입력에 대하여 의도 분석을 하는 프로그램입니다.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'tensorflow==2.14.0',
        'numpy==1.26.0',
        'pandas==2.0.3',
        'scikit-learn==1.4.0',
        'keras==2.14.0',
        'konlpy==0.6.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
#        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
