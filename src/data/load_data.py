import json
import os
import pprint
from pymongo import MongoClient


def load_data():
	"""
	"""
	# Restore MongoDB
	os.system('mongorestore --nsInclude \'trump.*\' --gzip "../../data/"')
	#client = MongoClient()
	#db = client.twitterdb


if __name__ == '__main__':
	load_data()