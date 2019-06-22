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


def get_engine(password: str, host: str, port: str, database: str):
    return sqlalchemy.create_engine(
        'postgresql+psycopg2://root:{}@{}:{}/{}'.format(
            password,
            host,
            port,
            database
        )
    )


def save_data(df: list, table: str):
    engine = get_engine(
        password='',
        host='localhost',
        port=5432,
        database=constants.DATABASE
    )
    dfl = DataFrame(df)

    dfl.to_sql(
        table,
        con=engine,
        index=False,
        if_exists='append',
        chunksize=100
    )

    return True


def get_election_data(election):
    return {
        'year': election['year'],
        'uuid': election['uuid']
    }


def get_states_data(election):
    return reduce(
        lambda acc, state: acc + [ omit(obj=state, _key='coligations') ],
        election['states'],
        []
    )


def get_coligacoes_data(election):
    coligacoes = []

    for state in election['states']:
        coligacoes.append(reduce(
            lambda acc, coligaction: acc + [ omit(obj=coligaction, _key='parties') ],
            state['coligations'],
            []
        ))
    
    return coligacoes


def get_parties_data(election):
    parties = []

    for state in election['states']:
        for coligacao in state['coligations']:
            parties.append(reduce(
                lambda acc, party: acc + [ omit(obj=party, _key='candidates') ],
                coligacao['parties'],
                []
            ))
    
    return parties


def get_candidates_data(election):
    candidates = []

    for state in election['states']:
        for coligacao in state['coligations']:
            for party in coligacao['parties']:
                candidates.append(party['candidates'])
    
    return candidates


def main():
    logging.info('Iniciando processamento de JSON de dados para SQL')

    logging.info('Verificando primeiro se json de dados existe')

    if not os.path.exists(constants.JSON_OUTPUT_PATH):
        logging.info('Arquivo não existe')
        return None
    
    with open(constants.JSON_OUTPUT_PATH) as _json:
        elections = json.load(_json)

        elections_df = flatten([ get_election_data(election=election) for election in elections ])

        states_df = flatten([ get_states_data(election=election) for election in elections ])

        coligations_df = flatten_deep([ get_coligacoes_data(election=election) for election in elections ])

        parties_df = flatten_deep([ get_parties_data(election=election) for election in elections ])

        candidates_df = flatten_deep([ get_candidates_data(election=election) for election in elections ])

        logging.info('Salvando dados das eleições')
        save_data(df=elections_df, table='tb_elections')

        logging.info('Salvando dados dos estados')
        save_data(df=states_df, table='tb_states')

        logging.info('Salvando dados das coligações')
        save_data(df=coligations_df, table='tb_coligations')

        logging.info('Salvando dados dos partidos')
        save_data(df=parties_df, table='tb_parties')

        logging.info('Salvando dados dos candidatos')
        save_data(df=candidates_df, table='tb_delegates')


if __name__ == "__main__":
    main()
