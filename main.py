import logging
import os
import pandas as pd
from constants import FORMAT_FILE, OUTPUT_PATH, CANDIDATES_CSV
from parser import generate_party_data
from helpers import save_data

"""
Etapas

- Checar se o arquivo do turicas esta na pasta data/input
  - Não estando, aborta dizendo o motivo
- Checar se o arquivo CSV gerado pelo scrapping da página da câmera existe
  - Não existindo, faça o download
    link: https://www.camara.leg.br/internet/agencia/infograficos-html5/DeputadosEleitos/index.html
"""

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(module)s-l.%(lineno)s]%(asctime)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    logging.info('Iniciando procedimento')
    filepath = f'{OUTPUT_PATH}/{CANDIDATES_CSV}{FORMAT_FILE}'
    logging.info('Checando se o arquivo de dados consolidados por deputado existe')

    if os.path.exists(filepath):
        logging.info('Arquivo existe')
    else:
        logging.info('Arquivo não existe')
        data = pd.DataFrame(generate_party_data())
        logging.info('Salvando dados')
        save_data(df=data, filepath=filepath)

if __name__ == '__main__':
    main()
