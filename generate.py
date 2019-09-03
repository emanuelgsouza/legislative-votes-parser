import pandas as pd
from pandas import DataFrame, Series
import pydash
import logging
import os
import constants
import helpers
import json
import uuid
from functools import reduce

"""
Arquivo para transformar os dados dos CSVs para um único arquivo JSON, chamado data.json
"""

logging.basicConfig(
    level=logging.INFO,
    format='[%(module)s-l.%(lineno)s]%(asctime)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def get_party_item(sigla, df_c, df_p):
    if len(df_p[df_p['sigla_partido'] == sigla]) > 0:
        return df_p[df_p['sigla_partido'] == sigla].iloc[0]

    if len(df_c[df_c['sigla_partido'] == sigla]) > 0:
        return df_c[df_c['sigla_partido'] == sigla].iloc[0]    
    
    return {}


def use_in_reduce(acc: str, part: str):
    # primeira iteracao
    if len(acc) == 0:
        return acc + part.capitalize()
    
    # evitar que nomes com DA e DE, fique Da e De
    if part.upper() in ['DE', 'DA']:
        return acc + ' ' + part.lower()

    # iteracoes subsequentes
    return acc + ' ' + part.capitalize()


def normalize_nome(nome: str):
    if len(nome.split(' ')) == 1:
        return nome.capitalize()
    
    return reduce(
        use_in_reduce,
        nome.split(' '),
        ''
    )


def factory_candidate(
    candidate: Series,
    party_uuid: str,
    coeciente_eleitoral: int,
    coligation_uuid=str,
    state_uuid=str,
    year_uuid=str
):
    status = candidate['descricao_totalizacao_turno']
    votes = int(candidate['total_votos'])

    return {
        'uuid': str(str(uuid.uuid4())),
        'party_uuid': str(party_uuid),
        'coligation_uuid': str(coligation_uuid),
        'state_uuid': str(state_uuid),
        'year_uuid': str(year_uuid),
        'name': normalize_nome(nome=candidate['nome']),
        'urne_name': normalize_nome(nome=candidate['nome_urna']),
        'number': int(candidate['numero_urna']),
        'votes': votes,
        'sigla_party': candidate['sigla_partido'],
        'state_sigla': candidate['sigla_uf'],
        'year': int(candidate['ano_eleicao']),
        'not_is_pulling': votes >= coeciente_eleitoral,
        'status': status
    }


def generate_candidate_data(
    df_c: DataFrame,
    party_uuid: str,
    coeciente_eleitoral: int,
    sigla: str,
    coligation_uuid=str,
    state_uuid=str,
    year_uuid=str
):
    candidates = df_c[df_c['sigla_partido'] == sigla]

    return DataFrame([
        factory_candidate(
            candidate=candidate,
            party_uuid=party_uuid,
            coeciente_eleitoral=coeciente_eleitoral,
            coligation_uuid=coligation_uuid,
            state_uuid=state_uuid,
            year_uuid=year_uuid
        ) for (_, candidate) in candidates.iterrows()
    ])


def factory_party(
    sigla: str,
    df_c: DataFrame,
    df_p: DataFrame,
    coligation_uuid: str,
    coeciente_eleitoral: int,
    state_uuid=str,
    year_uuid=str
):
    logging.debug(f'Analisando o partido {sigla}')
    item = get_party_item(sigla=sigla, df_c=df_c, df_p=df_p)
    legend_key = 'total_legenda'
    total_legenda = int(item[legend_key]) if legend_key in item.keys() else 0
    party_uuid = uuid.uuid4()
    candidates = generate_candidate_data(
        df_c=df_c,
        party_uuid=party_uuid,
        coeciente_eleitoral=coeciente_eleitoral,
        sigla=item['sigla_partido'],
        coligation_uuid=coligation_uuid,
        state_uuid=state_uuid,
        year_uuid=year_uuid
    )

    if len(candidates) == 0:
        return {
            'uuid': str(party_uuid),
            'state_uuid': str(state_uuid),
            'year_uuid': str(year_uuid),
            'coligation_uuid': str(coligation_uuid),
            'name': normalize_nome(nome=item['nome_partido']),
            'year': int(item['ano_eleicao']),
            'state_sigla': item['sigla_uf'],
            'initials': item['sigla_partido'],
            'number': int(item['numero_partido']),
            'votes': 0,
            'elect_qty': 0,
            'suplent_qty': 0,
            'not_pulling_qty': 0,
            'legend_votes': total_legenda,
            'candidates': []
        }

    return {
        'uuid': str(party_uuid),
        'state_uuid': str(state_uuid),
        'year_uuid': str(year_uuid),
        'coligation_uuid': str(coligation_uuid),
        'name': normalize_nome(nome=item['nome_partido']),
        'year': int(item['ano_eleicao']),
        'state_sigla': item['sigla_uf'],
        'initials': item['sigla_partido'],
        'number': int(item['numero_partido']),
        'votes': int(sum(candidates['votes'])),
        'elect_qty': len(candidates[candidates['status'].isin(constants.ELECT_CONDITIONS)]),
        'suplent_qty': len(candidates[candidates['status'].isin(constants.SUPLENT_CONDITIONS)]),
        'not_pulling_qty': len(candidates[candidates['not_is_pulling']]),
        'candidates': len(candidates),
        'legend_votes': total_legenda,
        'candidates': list(candidates.to_dict(orient='index').values())
    }


def generate_party_data(
    siglas: list,
    df_c=DataFrame,
    df_p=DataFrame,
    coligation_uuid=str,
    coeciente_eleitoral=int,
    state_uuid=str,
    year_uuid=str
):
    return [
        factory_party(
            sigla=sigla,
            df_c=df_c,
            df_p=df_p,
            coligation_uuid=coligation_uuid,
            coeciente_eleitoral=coeciente_eleitoral,
            state_uuid=state_uuid,
            year_uuid=year_uuid
        )
        for sigla in siglas
    ]


def factory_coligation(
    coligation=str,
    df_p=DataFrame,
    df_c=DataFrame,
    state_uuid=str,
    coeciente_eleitoral=int,
    year_uuid=str
):
    item = df_p[df_p['composicao_legenda'] == coligation].iloc[0]
    siglas = helpers.get_parties_by_coligation(coligation)

    logging.debug(f'Analisando a coligação {coligation}')
    logging.debug(f'Foram encontrados {len(siglas)} partidos')
    coligation_uuid = uuid.uuid4()

    parties = generate_party_data(
        siglas=siglas,
        df_c=df_c,
        df_p=df_p,
        coligation_uuid=coligation_uuid,
        coeciente_eleitoral=coeciente_eleitoral,
        state_uuid=state_uuid,
        year_uuid=year_uuid
    )

    return {
        'uuid': str(coligation_uuid),
        'year_uuid': str(year_uuid),
        'state_uuid': str(state_uuid),
        'state_sigla': item['sigla_uf'],
        'year': int(item['ano_eleicao']),
        'name': normalize_nome(nome=item['nome_legenda']),
        'composition': coligation,
        'isolated_party': True if len(siglas) == 1 else False,
        'elect_qty': len(df_c[df_c['descricao_totalizacao_turno'].isin(constants.ELECT_CONDITIONS)]),
        'suplent_qty': len(df_c[df_c['descricao_totalizacao_turno'].isin(constants.SUPLENT_CONDITIONS)]),
        'candidates': len(df_c),
        'not_pulling_qty': sum(
            map(lambda x: int(x.get('not_pulling_qty', 0)), parties)
        ),
        'parties': parties
    }

def generate_coligation_data(
    coligations: list,
    df_c: DataFrame,
    df_p: DataFrame,
    state_uuid: str,
    coeciente_eleitoral: int,
    year_uuid=str
):
    return [
        factory_coligation(
            coligation=col,
            df_c=df_c,
            df_p=df_p,
            state_uuid=state_uuid,
            coeciente_eleitoral=coeciente_eleitoral,
            year_uuid=year_uuid
        )
        for col in coligations
    ]

def generate_date_for_state(state: str, df_c: DataFrame, df_p: DataFrame, ano: int, year_uuid: str):
    logging.info(f'Analizando o estado {state}')

    candidates_by_state = df_c[df_c['sigla_uf'] == state]
    parties_by_state = df_p[df_p['sigla_uf'] == state]

    logging.info(f'Foram encontrados {len(candidates_by_state)} candidatos em {len(parties_by_state)} partidos')

    cadeiras = len(candidates_by_state[candidates_by_state['descricao_totalizacao_turno'].isin(constants.ELECT_CONDITIONS)])
    votos_nominais = int(sum(parties_by_state['total_votos']))
    legend_votes = int(sum(parties_by_state['total_legenda']))

    coeciente_eleitoral = int((votos_nominais + legend_votes) / cadeiras)

    state_uuid = uuid.uuid4()

    coligations = generate_coligation_data(
        coligations=helpers.get_legend_composition(parties_by_state),
        df_c=candidates_by_state,
        df_p=parties_by_state,
        state_uuid=state_uuid,
        coeciente_eleitoral=coeciente_eleitoral,
        year_uuid=year_uuid
    )

    return {
        'uuid': str(state_uuid),
        'election_uuid': str(year_uuid),
        'name': normalize_nome(nome=candidates_by_state['descricao_ue'].iloc[0]),
        'sigla': state,
        'year': int(ano),
        'nominal_votes': votos_nominais,
        'legend_votes': legend_votes,
        'chars': cadeiras,
        'election_quotient': coeciente_eleitoral,
        'not_pulling_qty': sum(
            map(lambda coligation: coligation.get('not_pulling_qty', 0), coligations)
        ),
        'coligations': coligations
    }


def generate_ano_data(ano: int, df_c: DataFrame, df_p: DataFrame, res_json: list):
    year_uuid = uuid.uuid4()

    states = [
        generate_date_for_state(
            state=state,
            df_c=df_c[df_c['ano_eleicao'] == ano],
            df_p=df_p[df_p['ano_eleicao'] == ano],
            ano=ano,
            year_uuid=year_uuid
        )
        for state in helpers.get_states(df=df_c)
    ]

    res_json.append({
        'year': ano,
        'uuid': str(year_uuid),
        'is_federal': ano in constants.FEDERAL_ELECTIONS,
        'not_pulling_qty': helpers.get_sum_prop(states, 'not_pulling_qty'),
        'legend_votes': helpers.get_sum_prop(states, 'legend_votes'),
        'nominal_votes': helpers.get_sum_prop(states, 'nominal_votes'),
        'chars': helpers.get_sum_prop(states, 'chars'),
        'states': states
    })

def main():
    logging.info('Iniciando procedimento de geração dos dados para o banco')
    logging.info('Carregando os dados dos partidos')

    df_p = None
    df_c = None
    res_json = []

    if not os.path.exists(constants.PARTIDO_FILE_PATH):
        logging.info('Arquivo de partidos não existe')
        return None
    else:
        df_p = pd.read_csv(constants.PARTIDO_FILE_PATH)
    
    if not os.path.exists(constants.CANDIDATO_FILE_PATH):
        df_p = None
        logging.info('Arquivo de candidatos não existe')
        return None
    else:
        df_c = pd.read_csv(constants.CANDIDATO_FILE_PATH)
    
    logging.info('Dados carregados')

    for ano in [2018]:
        generate_ano_data(
            ano=ano,
            df_c=df_c,
            df_p=df_p,
            res_json=res_json
        )
    
    with open(constants.JSON_OUTPUT_PATH, 'w') as fp:
        json.dump(res_json, fp, indent=2)

if __name__ == '__main__':
    main()
