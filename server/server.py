#!/usr/bin/env python2
"""
Server code to track number of visitors.
"""
import logging
import json
import time
from flask import Flask, request, send_from_directory, g, redirect, url_for
from flask import jsonify
from pymongo import MongoClient

QUIZ_TYPES = set(['men', 'women'])

app = Flask(__name__)


def connect_db():
    """Connects to the signinucsd database on mlab servers."""
    db = MongoClient(app.config['DATABASE'])
    return db


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'dbConnection'):
        g.dbConnection = connect_db()
    return g.dbConnection[app.config['DATABASE_NAME']]


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'dbConnection'):
        g.dbConnection.close()


@app.route('/')
def index():
    db = get_db()
    visits_col = db.visits
    visits_col.find_one_and_update(
        {'_id': 'visits'},
        {'$inc': {'count': 1}},
        upsert=True)

    logging.info("IP Address: {}".format(request.remote_addr))

    return send_from_directory('static', 'html/quiz_men_1.html')


@app.route('/quiz/<quiz_type>')
def quiz(quiz_type):
    if quiz_type not in QUIZ_TYPES:
        logging.warning("Incorrect Quiz Type: '{}'".format(quiz_type))

    args = request.args
    if 'version' not in args:
        logging.warning("'version' not in args.")
        return "'version' not in args."

    version = int(args['version'])

    if quiz_type == 'men':
        if version == 0:
            return send_from_directory('static', 'html/index.html')
        elif version == 1:
            return send_from_directory('static', 'html/quiz_men_1.html')
        else:
            logging.warning("Version does not exist: '{}'".format(version))
            return "Version does not exist: '{}'".format(version)

    elif quiz_type == 'women':
        logging.warning("Women quiz not available yet.")
        return "Version does not exist: '{}'".format(version)


@app.route('/data', methods=['POST'])
def handle_survey_answers():
    """
    Receives form data adds submission to database.
    """
    entry = json.loads(request.form['data'])

    timestamp = time.time()
    entry['timestamp_secs'] = timestamp

    entry_string = json.dumps(entry, indent=4, sort_keys=True)
    logging.debug(entry_string)

    db = get_db()

    form_type = entry['form_type']

    responses_col = None

    # Differentiate between men and women quiz.
    if form_type == 'men':
        responses_col = db.responses_men
    elif form_type == 'women':
        responses_col = db.responses_women
    else:
        logging.warning("Form Type is not 'men' or 'women': {}".format(
            form_type))

    # Update responses counter.
    responses_col.find_one_and_update(
        {'_id': 'responses'},
        {'$inc': {'count': 1}},
        upsert=True)

    # Insert the response information.
    response_id = responses_col.insert_one(entry).inserted_id

    resp = {"id": str(response_id)}

    return jsonify(resp)


@app.route('/analytics')
def analytics():
    db = get_db()
    visits_col = db.visits
    visit_count = visits_col.find_one(
        {'_id': 'visits'})

    return jsonify(visit_count)


def main(args):
    if args.no_log:
        log_file_path = None
    else:
        log_file_path = 'sadscore.log'

    logging.basicConfig(filename=log_file_path, level=logging.INFO)

    if args.prod:
        import db_key_prod as db_key
        print("Running in PRODUCTION")
    else:
        import db_key_dev as db_key
        print("Running in DEVELOPMENT")

    # Load default config and override config from an environment variable
    app.config.update(dict(
        DATABASE=db_key.dbKey,
        USERNAME=db_key.username,
        PASSWORD=db_key.password,
        DATABASE_NAME=db_key.db_name
    ))

    app.run(
        host='0.0.0.0',
        debug=args.debug,
        port=args.port)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('-p', '--port',
                        help="Port that the server will run on.",
                        type=int,
                        default=5050)
    parser.add_argument('-d', '--debug',
                        help="Whether or not to run in debug mode.",
                        default=False,
                        action='store_true')
    parser.add_argument('--prod',
                        help="Whether or not to run in prod mode.",
                        default=False,
                        action='store_true')

    parser.add_argument('--no_log',
                        help="Whether to not keep logs.",
                        default=False,
                        action='store_true')

    args = parser.parse_args()
    main(args)
