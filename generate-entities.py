from pandas import DataFrame
import sqlalchemy
import constants
import json
import logging
import os
import helpers
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


def get_entity_path(entity: str) -> str:
    return f"{constants.ENTITIES_OUTPUT}/{entity}.json"


def get_state_data(elections: dict):
    states = []
    for election in elections:
        states += list(map(lambda state: helpers.omit(state, 'coligations'), election.get('states', [])))
    
    return states


def get_election_data(election: dict):
    return helpers.omit(election, 'states')


def main():
    logging.info('Iniciando processamento de JSON de dados para SQL')

    logging.info('Verificando primeiro se json de dados existe')

    if not os.path.exists(constants.JSON_OUTPUT_PATH):
        logging.info('Arquivo não existe')
        return None
    
    logging.info('Verificando se diretorio de output dos JSONs existe')
    if not os.path.isdir(constants.ENTITIES_OUTPUT):
        logging.info('Diretorio de entities não existe, criando...')

        os.makedirs(constants.ENTITIES_OUTPUT)
    
    with open(constants.JSON_OUTPUT_PATH) as _json:
        data = json.load(_json)

        elections = []
        states = []
        coligations = []
        parties = []
        candidates = []
        candidates_not_pulling = []

        for election in data:
            elections += [helpers.omit(election, 'states')]
            
            for state in election.get('states', []):
                states += [helpers.omit(state, 'coligations')]

                for coligation in state.get('coligations', []):
                    coligations += [helpers.omit(coligation, 'parties')]

                    for party in coligation.get('parties', []):
                        parties += [helpers.omit(party, 'candidates')]

                        for candidate in party.get('candidates', []):
                            candidates += [candidate]

                            if candidate['not_is_pulling']:
                                candidates_not_pulling += [candidate]
        
        logging.info('Salvando dados para a entidade eleição')
        check_exists_and_save(obj=elections, path=get_entity_path(entity='elections'))

        logging.info('Salvando dados para a entidade estado')
        check_exists_and_save(obj=states, path=get_entity_path(entity='states'))

        logging.info('Salvando dados para a entidade coligação')
        check_exists_and_save(obj=coligations, path=get_entity_path(entity='coligations'))

        logging.info('Salvando dados para a entidade partido')
        check_exists_and_save(obj=parties, path=get_entity_path(entity='parties'))
    
        logging.info('Salvando dados para a entidade candidato')
        check_exists_and_save(obj=candidates, path=get_entity_path(entity='candidates'))

        logging.info('Salvando dados com a listagem de candidatos que não foram puxados')
        check_exists_and_save(obj=candidates_not_pulling, path=get_entity_path(entity='candidates_not_pulling'))

if __name__ == "__main__":
    main()
