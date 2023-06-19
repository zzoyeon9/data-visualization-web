#-*- coding:utf-8 -*-

"""Front Main
"""

#
# Imports Modules
#
import argparse
import sys
from modules.dependency import check_dependencies
try:
    check_dependencies()
except:
    message = "Cannot run tFront Service."
    print(message, file=sys.stderr)
    sys.exit(-1)
from modules.service import Service
from db.connection import Connection

#
# DB(PostgreSQL) Connection
#

#conn = psycopg2.connect(host="10.1.16.129", port=5432, dbname="test", user="postgres", password="hansol2014")

db = Connection()

#connect()


#
# Front Main
#
parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='10.0.1.47')
parser.add_argument('--port', type=int, default=30000)
args = parser.parse_args()
params = {
    "host": args.host,
    "port": args.port,
    "reload": True,
}
servie = Service()
servie.run_forever(**params)

