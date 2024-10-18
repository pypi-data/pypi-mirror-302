from setuptools import setup, find_packages

setup(
    name='FileBrowse',
    version='0.1.1',
    description='A simple library to browse and select files without creating a GUI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jatin Gera',
    author_email='gera.jatin@gmail.com',
    url='https://github.com/jgera/filebrowse',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
