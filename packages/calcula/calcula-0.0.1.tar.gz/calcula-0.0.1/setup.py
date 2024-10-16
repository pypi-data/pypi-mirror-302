from setuptools import setup, find_packages

setup(
    name='calcula',  # Nome do pacote
    version='0.0.1',  # Versão inicial
    description='Uma calculadora simples que suporta operações básicas em Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='elvingup', 
    author_email='el.cayro@gmail.com', 
    url='https://github.com/elvingup/calcula-01.git',  
    py_modules=['calcula'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'calcula = calcula:calcula',  # Comando de entrada (opcional)
        ],
    },
)
