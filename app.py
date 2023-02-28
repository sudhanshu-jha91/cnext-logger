from flask import Flask, request, jsonify
from infi.clickhouse_orm import Database, make_model_instance, select, make_connection
from math import ceil
from datetime import datetime

app = Flask(__name__)

app = Flask(__name__)

app.config.from_pyfile('config.py')

connection = make_connection(
    host=app.config['CLICKHOUSE_HOST'],
    port=app.config['CLICKHOUSE_PORT'],
    database=app.config['CLICKHOUSE_DATABASE'],
    user=app.config['CLICKHOUSE_USER'],
    password=app.config['CLICKHOUSE_PASSWORD']
)

db = Database(connection)


@app.route('/log-ingest', methods=['POST'])
def log():
    data = {}
    data = request.get_json()
    log = LogData(
        id=data.get('id'),
        level=data.get('level'),
        message=data.get('message'),
        extra_info=data.get('extra_info'),
        source=data.get('source'),
        created_at=datetime.now(),
    )
    db.insert([log])
    return data, 201


@app.route('/logs', methods=['GET'])
def get_logs():
    # Get the requested page number and page size from the query string, with default values of 1 and 20, respectively.

    page = request.args.get('page', default=1, type=int)
    # page_size = request.args.get('page_size', default=20, type=int)
    # # Initialize the query and params list with a base SELECT statement that includes all fields from the logs table.
    query = f'SELECT * FROM log_data WHERE 1 = 1'
    params = []

    if 'level' in request.args:
        query += ' AND level = %s'
        params.append(request.args['level'])
    if 'message' in request.args:
        query += ' AND message LIKE %s'
        params.append(f'%{request.args["message"]}%')
    if 'search' in request.args:
        search = request.args['search']
        query += ' AND ('
        query += ' OR '.join(['message LIKE %s', 'level LIKE %s', 'extra_info LIKE %s', 'source LIKE %s'])
        query += ')'
        params.extend([f'%{search}%']*4)

    logs_count = db.count(query, params=params)
    total_pages = ceil(logs_count / page_size)
    offset = (page - 1) * page_size
    logs = select(db, f'{query} ORDER BY created_at DESC LIMIT {page_size} OFFSET {offset}', params=params)

    return jsonify({
        'logs': [log.to_dict() for log in logs],
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages
    })

if __name__ == '__main__':
    app.run()
