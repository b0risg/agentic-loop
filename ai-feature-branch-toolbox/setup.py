from setuptools import setup, find_packages

setup(
    name="ai_feature_branch_toolbox",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "GitPython",
        "PyYAML",
    ],
    author="BORiS",  # INPUT_REQUIRED {Your actual name}
    author_email="borisjg@gmail.com",  # INPUT_REQUIRED {Your actual email}
    description="A library for AI agents to interact with Git repositories and apply feature branch based development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/b0risg/workspace",  # INPUT_REQUIRED {Your actual GitHub repository URL}
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'ai-feature-branch-toolbox=ai_feature_branch_toolbox.cli:main',
        ],
    },
)