import logging
import os
import pandas as pd
import constants
from parser import generate_party_data, generate_candidate_data
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
    logging.info('Checando se o arquivo de dados consolidados por partido existe')

    # TODO: verificar também se o arquivo de input consta em data/input
    if os.path.exists(constants.PARTIDO_FILE_PATH):
        logging.info('Arquivo existe')
    else:
        logging.info('Arquivo não existe')
        data = pd.DataFrame(generate_party_data())
        logging.info('Salvando dados')
        save_data(df=data, filepath=constants.PARTIDO_FILE_PATH)
    
    # TODO: verificar também se o arquivo de input consta em data/input
    logging.info('Checando se o arquivo de dados consolidados por candidato existe')
    if os.path.exists(constants.CANDIDATO_FILE_PATH):
        logging.info('Arquivo existe')
    else:
        logging.info('Arquivo não existe')
        data = pd.DataFrame(generate_candidate_data())
        logging.info('Salvando dados')
        save_data(df=data, filepath=constants.CANDIDATO_FILE_PATH)

if __name__ == '__main__':
    main()
