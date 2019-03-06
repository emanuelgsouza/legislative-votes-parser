FORMAT_FILE = '.csv'

INPUT_PATH = 'data/input'
PARTIDO_MUNZONA = 'votacao-partido-zona'
CANDIDATO_MUNZONA = 'votacao-zona'

OUTPUT_PATH = 'data/output'
PARTIDO_CSV = 'votos_consolidados_por_partido'
CANDIDATO_CSV = 'votos_consolidados_por_deputado'

PARTIDO_FILE_PATH = f'{OUTPUT_PATH}/{PARTIDO_CSV}{FORMAT_FILE}'
CANDIDATO_FILE_PATH = f'{OUTPUT_PATH}/{CANDIDATO_CSV}{FORMAT_FILE}'
JSON_OUTPUT_PATH = f'{OUTPUT_PATH}/data.json'

DATABASE = 'db_elections'

FEDERAL_ELECTIONS = [2018]

ELECT_CONDITIONS = ['ELEITO POR QP', 'ELEITO POR MEDIA']

SUPLENT_CONDITIONS = ['SUPLENTE']

ELECTIONS_OUTPUT = f'{OUTPUT_PATH}/elections'

STATES = [
    'AC',
    'AL',
    'AM',
    'AP',
    'BA',
    'CE',
    'DF',
    'ES',
    'GO',
    'MA',
    'MG',
    'MS',
    'MT',
    'PA',
    'PB',
    'PE',
    'PI',
    'PR',
    'RJ',
    'RN',
    'RO',
    'RR',
    'RS',
    'SC',
    'SE',
    'SP',
    'TO',
    'ZZ'
]
