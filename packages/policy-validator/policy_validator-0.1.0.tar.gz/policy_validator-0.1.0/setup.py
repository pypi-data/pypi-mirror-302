from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='policy_validator',
    version='0.1.0',
    author='Ashkan Rafiee',
    author_email='ashkanrafiee-pypi.cheer081@passmail.net',
    description='A policy validation tool using OpenAI Models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ashkanrafiee/policy_validator',
    packages=['policy_validator'],
    package_dir={'': 'src'},
    install_requires=[
        'openai>=1.47.0',
        'tenacity>=9.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    keywords=['openai', 'GPT', 'policy validation', 'content moderation']
)
