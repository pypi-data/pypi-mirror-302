import os
from setuptools import setup, find_packages
base_dir = os.path.dirname(os.path.abspath(__file__))


def get_long_description():
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, encoding="utf-8") as readme_file:
        return readme_file.read()


def get_project_version():
    version_path = os.path.join(base_dir, "dspeech", "version.py")
    version = {}
    with open(version_path, encoding="utf-8") as fp:
        exec(fp.read(), version)
    return version["__version__"]


def get_requirements(path):
    with open(path, encoding="utf-8") as requirements:
        return [requirement.strip() for requirement in requirements]


install_requires = get_requirements(os.path.join(base_dir, "requirements.txt"))
conversion_requires = get_requirements(
    os.path.join(base_dir, "requirements.conversion.txt")
)

setup(
    name='dspeech',
    version=get_project_version(),
    description='A Speech-to-Text toolkit with VAD, punctuation, and emotion classification',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Zhao Sheng',
    author_email='zhaosheng@nuaa.edu.cn',
    url='https://gitee.com/iint/dspeech',
    keywords='speech-to-text, speech processing, speech recognition, speech synthesis, speech',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'dspeech=dspeech.cli:main',  # 将 CLI 绑定到 dspeech 命令
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    extras_require={
        "conversion": conversion_requires,
        "dev": [
            "black==23.*",
            "flake8==6.*",
            "isort==5.*",
            "pytest==7.*",
        ],
    },
    include_package_data=True,
    python_requires='>=3.10',
)
