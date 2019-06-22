import logging
import os
import pandas as pd
import constants
import parser
from helpers import save_data

"""
Arquivo de consolidação dos CSVs do TSE para:
- votos_consolidados_por_deputado.csv
- votos_consolidados_por_partido.csv
"""

logging.basicConfig(
    level=logging.INFO,
    format='[%(module)s-l.%(lineno)s]%(asctime)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    logging.info('Iniciando procedimento')
    logging.info('Checando se o arquivo de dados consolidados por partido existe')

    if os.path.exists(constants.PARTIDO_FILE_PATH):
        logging.info('Arquivo existe')
    else:
        logging.info('Arquivo não existe')
        data = pd.DataFrame(parser.generate_party_data())
        logging.info('Salvando dados')
        save_data(df=data, filepath=constants.PARTIDO_FILE_PATH)
    
    logging.info('Checando se o arquivo de dados consolidados por candidato existe')
    if os.path.exists(constants.CANDIDATO_FILE_PATH):
        logging.info('Arquivo existe')
    else:
        logging.info('Arquivo não existe')
        data = pd.DataFrame(parser.generate_candidate_data())
        logging.info('Salvando dados')
        save_data(df=data, filepath=constants.CANDIDATO_FILE_PATH)

if __name__ == '__main__':
    main()
