import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import constants
import json
import logging
import sys


logging.basicConfig(
	level=logging.INFO,
	format='[%(module)s-l.%(lineno)s]%(asctime)s: %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)


entities = [
	'elections',
	'states',
	'coligations'
	'parties',
	'delegates'
]


def get_db():
	if os.path.exists(constants.FIREBASE_ADMIN_CREDENTIALS):
		cred = credentials.Certificate('./firebase.json')

		firebase_admin.initialize_app(cred)

		return firestore.client()
	
	raise Exception('Firebase SKD credentials not found')


def load_entity_data(entity: str) -> list:
	ENTITY_PATH = f'{constants.OUTPUT_PATH}/entities/{entity}.json'

	if os.path.exists(ENTITY_PATH):
		with open(ENTITY_PATH) as data:
			elections = json.load(data)

		return elections
	
	return []


def main():
	try:
		db = get_db()

		for entity in entities:
			logging.info(f'Processing {entity} entity...')
			entity_data = load_entity_data(entity)
			docs = len(entity_data)
			logging.info(f'Found {docs} docs')
			count = 1

			for doc in entity_data:
				logging.info(f'Uploading {count}/{docs}')
				try:
					uuid = doc.get('uuid')
					db.collection(entity).document(uuid).set(doc)

					logging.info('Upload successfully')
				except:
					logging.error('An error ocurred')
					logging.error(sys.exc_info())
			
				count += 1
			
			logging.info('')
	except:
		logging.error('An error ocurred')
		logging.error(sys.exc_info())

if __name__ == '__main__':
	main()
