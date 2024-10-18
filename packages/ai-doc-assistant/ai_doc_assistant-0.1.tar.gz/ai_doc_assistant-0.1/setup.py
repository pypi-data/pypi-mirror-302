from setuptools import setup, find_packages

setup(
    name='ai_doc_assistant',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'transformers',
        'scikit-learn',
        'markdown'
    ],
    author='Your Name',
    author_email='thamimansari358@gmail.com',
    description='AI-Powered Documentation Assistant for generating code documentation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
