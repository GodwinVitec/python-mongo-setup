import argparse
from pymongo import MongoClient
import os
from dotenv import load_dotenv

from models.Company import Company
from models.Trainee import Trainee

# Create the parser
parser = argparse.ArgumentParser(description='create or drop collections.')

# Add the arguments
parser.add_argument('direction', metavar='U', type=str,
                    help='up => create collections, down => drop collections')

# Parse the arguments
args = parser.parse_args()
direction = args.direction

if direction not in ['up', 'down', 'update']:
    raise Exception("Invalid argument: ", args)

load_dotenv()

uri = os.getenv("CONNECTION_STRING")
database_name = os.getenv("DATABASE_NAME")
client = MongoClient(uri)


def up(db_models):
    try:
        for model in db_models:
            model.up()

        print('Successfully created collections.')
    except Exception as up_error:
        raise Exception("Unable to create collections due to the following error: ", up_error)


def update(db_models):
    try:
        for model in db_models:
            model.update()

        print('Successfully updated collections.')
    except Exception as down_error:
        raise Exception("Unable to update collections due to the following error: ", down_error)


def down(db_models):
    try:
        for model in db_models:
            model.down()

        print('Successfully dropped collections.')
    except Exception as down_error:
        raise Exception("Unable to drop collections due to the following error: ", down_error)


try:
    database = client.get_database(database_name)
    create_models = [Company(database), Trainee(database)]
    update_models = [Company(database), Trainee(database)]
    drop_models = [Trainee(database), Company(database)]

    if direction == 'up':
        up(create_models)
    elif direction == 'down':
        down(drop_models)
    else:
        update(update_models)

    client.close()
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)
