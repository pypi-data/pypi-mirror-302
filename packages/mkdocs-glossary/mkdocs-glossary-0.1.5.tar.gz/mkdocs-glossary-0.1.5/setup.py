import io

from setuptools import setup, find_packages

setup(
    name='mkdocs-glossary',
    version='0.1.5',
    description='A MkDocs plugin that automatically creates references to glossary terms within italicized text from a specified glossary list file.',
    long_description=io.open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    keywords='mkdocs',
    url='https://gitlab.com/thiti-mkdocs-plugins/mkdocs-glossary',
    author='Thibaud Briard',
    author_email='thiti517@outlook.com',
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'mkdocs>=1.4.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'glossary = mkdocs_glossary.plugin:Glossary'
        ]
    }
)