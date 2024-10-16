from setuptools import setup, find_packages

setup(
    name='mzr_ingestions',
    version='0.1',
    packages=find_packages(),  # Isso irá incluir todos os pacotes no diretório
    install_requires=[
        'getdaft==0.3.4',      # Versão exata do Daft que está funcionando
        'pyarrow==17.0.0',     # Versão exata do PyArrow
        'requests==2.32.3',    # Versão exata do Requests
        'ipython',             # Versão mais recente do IPython
        'python-dotenv',       # Para lidar com variáveis de ambiente
        'pandas==2.2.3',       # Versão exata do Pandas
        'numpy==2.1.1',        # Versão exata do NumPy
        'fsspec==2023.12.2',   # Para acessar sistemas de arquivos
        's3fs==2023.12.2'      # Para acessar S3 diretamente
    ],
    author='Douglas Borges Martins',
    author_email="douglas@meizter.com",
    description='pacote para manipulação do Dremio',
)
