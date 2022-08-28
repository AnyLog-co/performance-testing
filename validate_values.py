import datetime
import requests

CONN = '172.105.37.122:32149'
DB_NAME = 'test'
TABLE_NAME = 'rand_data2'
EXPECT_RESULTS = {
    10000000: {
        'insert_time': datetime.timedelta(minutes=30),
        'increments_validiate': {}
    }
}
NUM_ROWS = 10000000


def get_results(query:str, sql:bool=True, networking:bool=True)->list:
    headers = {
        'User-Agent': 'AnyLog/1.23'
    }
    if sql is True:
        headers['command'] = f'sql {DB_NAME} format=json and stat=false "{query}"'
        print(f'sql {DB_NAME} format=json and stat=false "{query}"')
    if networking is True:
        headers['destination'] =  'network'
    try:
        r = requests.get(url=f'http://{CONN}', headers=headers)
    except Exception as error:
        print(f'Failed to execute GET against {CONN} | Query: {query} (Error: {error})')
        exit(1)
    else:
        if int(r.status_code) != 200:
            print(f'Failed to execute GET against {CONN} | Query: {query} (Network Error: {r.status_code})')
            exit(1)
        return r.json()['Query']


def test_row_count():
    """
    Validate all rows inserted
    :query:
        SELECT COUNT(*) FROM {TABLE_NAME}
    :assert:
        number of rows is as expected
    """
    query = f"SELECT COUNT(*) FROM {TABLE_NAME}"
    results = get_results(query=query, sql=True, networking=True)
    assert results[0]['count(*)'] == NUM_ROWS


def test_insert_time():
    """
    Validate length of time inserts took is less than (or equal to what's expected)
    :query:
        SELECT MIN(insert_timestamp) as min_ts, max(insert_timestamp) as max_ts FROM {TABLE_NAME}
    :assert:
        total amount of time inserts took
    """
    query = f"SELECT MIN(insert_timestamp) as min_ts, max(insert_timestamp) as max_ts FROM {TABLE_NAME}"
    results = get_results(query=query, sql=True, networking=True)
    min_ts = datetime.datetime.strptime(results[0]['min_ts'], '%Y-%m-%d %H:%M:%S.%f')
    max_ts = datetime.datetime.strptime(results[0]['max_ts'], '%Y-%m-%d %H:%M:%S.%f')
    assert max_ts - min_ts < EXPECT_RESULTS[NUM_ROWS]['insert_time']


def increments_validiate():
    # for hour in [1, 2, 6, 12, 24]:
    hour = 1
    query = (f"SELECT increments(hour, {hour}, timestamp), "
            +"min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_val, "
            +f"max(value) as max_val, avg(value) as avg_val, count(*) as row_count FROM {TABLE_NAME} "
            +"ORDER BY min_ts, max_ts")
    results = get_results(query=query, sql=True, networking=True)
    print(hour, results)

if __name__ == '__main__':
    increments_validiate()

