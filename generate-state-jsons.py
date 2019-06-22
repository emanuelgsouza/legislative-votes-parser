from pandas import DataFrame
import sqlalchemy
import constants
import json
import logging
import os
from helpers import omit
from functools import reduce
from operator import concat
from pydash import flatten, flatten_deep


logging.basicConfig(
    level=logging.INFO,
    format='[%(module)s-l.%(lineno)s]%(asctime)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def check_exists_and_save(obj, path):
    logging.info(f'Verificando se o arquivo {path} existe')

    if not os.path.isfile(path):
        logging.info('Arquivo não existe, criando...')

        save_to_json(obj=obj, path=path)


def save_to_json(obj, path):
    with open(path, 'w') as fp:
        json.dump(obj, fp, indent=2)

def main():
    logging.info('Iniciando processamento de JSON de dados para SQL')

    logging.info('Verificando primeiro se json de dados existe')

    if not os.path.exists(constants.JSON_OUTPUT_PATH):
        logging.info('Arquivo não existe')
        return None
    
    logging.info('Verificando se diretorio de output dos JSONs existe')
    if not os.path.isdir(constants.ELECTIONS_OUTPUT):
        logging.info('Diretorio de output dos JSONs nao existe, criando um')

        os.makedirs(constants.ELECTIONS_OUTPUT)
    
    with open(constants.JSON_OUTPUT_PATH) as _json:
        elections = json.load(_json)

        elections_to_save = []

        for election in elections:
            _path_year = f"{constants.ELECTIONS_OUTPUT}/{election['year']}"
            logging.info(f'Verificando se o diretório {_path_year} existe')

            if not os.path.isdir(_path_year):
                logging.info('Diretorio não existe, criando...')
                os.makedirs(_path_year)
            
            elections_to_save.append(omit(obj=election, _key='states'))
            
            states = election['states']

            for state in states:
                sigla = str(state['sigla']).lower()
                _path_state = f"{_path_year}/{sigla}.json"
                check_exists_and_save(obj=state, path=_path_state)
                
            
            logging.info('')
    
    path = f"{constants.ELECTIONS_OUTPUT}/elections.json"
    check_exists_and_save(obj=elections_to_save, path=path)

if __name__ == "__main__":
    main()
