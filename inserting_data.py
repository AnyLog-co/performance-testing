import argparse
import datetime
import json
import os
import random
import requests
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PROTOCOLS)

START_TIMESTAMP = datetime.datetime.utcnow()
SECOND_INCREMENTS = 0.864
ROWS_24h_INCREMENTS = 100000


def __insert_data(conn:str, db_name:str, payloads:str, processing_time:float)->bool:
    """
    Execute Insert data via REST PUT command
    :args:
        conn:str - REST connection information
        db_name:str - logical database name
        payloads:list - list of data to push into  AnyLog
        processing_time:float - historically how long data has been pushed into AnyLoog
    :params:
        status:bool
        header:dict - REST header information
        start_time:time.time - time in seconds
    :return:
        status + processing_time
    """
    status = True
    header = {
        'type': 'json',
        'dbms': db_name,
        'table': 'rand_data',
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    start_time = time.time()
    try:
        r = requests.put(url='http://%s' % conn, headers=header, data=payloads)
    except Exception as error:
        print(f'Failed to PUT data into {conn} (Error: {error})')
        status = False
    else:
        if int(r.status_code) != 200:
            print(f'Failed to PUT data into {conn}(Network Error: {r.status_code}')
            status = False
        else:
            processing_time += time.time() - start_time

    return status, processing_time


def __generate_row(total_rows:int, row_counter:int)->str:
    """
    Generate row to be inserted
    :global:
        START_TIMESTAMP:datetime.datetime - intial timestamp
        SECOND_INCREMENTS:float - Based on ROWS_24h_INCREMENTS, calculate increments for 24 hour period
        ROWS_24h_INCREMENTS:int - based number of rows in 24 hours
    :args:
        total_rows:int - total number of row to insert
        row_counter:int - current row to insert
    :params:
        seconds:float - increments size
        now:datetime.datetime - row timestamp
        row:dict - {timestamp, value} object to store in operator
    :return:
        row as JSON string
    """
    seconds = SECOND_INCREMENTS * (ROWS_24h_INCREMENTS/total_rows) * row_counter
    now = START_TIMESTAMP + datetime.timedelta(seconds=seconds)
    row = {'timestamp': now.strftime('%Y-%m-%d %H:%M:%S.%f'), 'value': round(random.random() * 100, 4)}

    return row


def __get_row_count(conn:str, db_name:str)->int:
    """
    Get row count
    :args:
        conn:str - REST connection info
        db_name:str - logical table name
    :params:
        header:dict - REST header
        r:requests.GET - request GET
    :return:
        row count
    """
    header = {
        'command': f'sql {db_name} stat=false and format=json select count(*) as row_count from rand_data;',
        "User-Agent": "AnyLog/1.23",
        "destination": "network"
    }
    try:
        r = requests.get(url='http://%s' % conn, headers=header)
    except Exception as error:
        print(f'Failed to execute GET against {conn} (Error: {error})')
    else:
        if int(r.status_code) != 200:
            print(f'FAiled to execute GET against {conn} (Error: {error})')
        else:
            try:
                return r.json()['Query'][0]['row_count']
            except Exception as error:
                return 0


def __insertion_time(conn:str, db_name:str)->datetime.timedelta:
    """
    Insert time
    :args:
        conn:str - REST connection info
        db_name:str - logical table name
    :params:
        format:str - insert_timestamp value format to covert from string to datetime
        header:dict - REST header information
        min_ts:datetime.datetime - min(insert_timestamp) value from SQL
        max_ts:datetime.datetime - max(insert_timestamp) value from SQL
    :return:
        difference between min insert_timestamp and max insert_timestamp
    """
    format = '%Y-%m-%d %H:%M:%S.%f'
    header = {
        "command": f'sql  {db_name} stat=false and format=json select min(insert_timestamp) as min_ts, max(insert_timestamp) as max_ts from rand_data;',
        "User-Agent": "AnyLog/1.23",
        "destination": "network"
    }
    try:
        r = requests.get(url='http://%s' % conn, headers=header)
    except Exception as error:
        print(f'Failed to execute GET against {conn} (Error: {error})')
    else:
        if int(r.status_code) != 200:
            print(f'FAiled to execute GET against {conn} (Error: {error})')
            return

    min_ts = datetime.datetime.strptime(r.json()['Query'][0]['min_ts'], format)
    max_ts = datetime.datetime.strptime(r.json()['Query'][0]['max_ts'], format)

    return max_ts - min_ts


def print_rows(total_rows:int):
    """
    Print rows N rows
    :args:
        row_counter:int - number of rows to print
    :params:
        row:str - generated row
    """
    for i in range(total_rows):
        row = __generate_row(total_rows=total_rows, row_counter=i)
        print(json.dumps(row))

def bkup_data(db_name:str, total_rows:int):
    file_name = f'{db_name}.rand_data.0.json'
    data = []
    for row in range(total_rows):
        data.append(json.dumps(__generate_row(total_rows=total_rows, row_counter=row)))

    for row in data:
        try:
            with open(file_name, 'w') as f:
                try:
                    f.write(row+"\n")
                except Exception as error:
                    print(f'Failed to append to {file_name} (Error: {error})')
        except Exception as error:
            print(f'Failed to open {file_name} (Error: {error})')


def insert_data(conn:str, total_rows:int, db_name:str)->int:
    """
    Process to insert data into AnyLog via REST
    :args:
        conn:str - REST connection information
        row_counter:int - total number of rows to insert
        db_name:str - logical table name
    :params:
        status:bool
        conns:list -
        data:list - generated row(s)
        insert_counter:int - number of insert processes that occured
        processing_time:float - amount of time insert processs(es) took
    :return:
        processing_time + insert_counter
    """
    conns = conn.split(',')
    conn_value = 0
    data = []
    insert_counter = 0
    processing_time = 0
    for i in range(total_rows):
        data.append(__generate_row(total_rows=total_rows, row_counter=i))
        if len(data) % 1000 == 0:
            status, processing_time = __insert_data(conn=conns[conn_value], db_name=db_name, payloads=json.dumps(data),
                                                processing_time=processing_time)
            if status is True:
                insert_counter += 1
            conn_value += 1
            if conn_value == len(conns):
                conn_value = 0
            data = []
    if len(data) != 0:
        status, processing_time = __insert_data(conn=conns[conn_value], db_name=db_name,
                                                payloads=json.dumps(data), processing_time=processing_time)
        if status is True:
            insert_counter += 1

    return processing_time, insert_counter


def insert_time(conn:str, total_rows:int, db_name:str):
    """
    Calculate AnyLong insert time
    :note:
        if not all rows inserted wait 30 secs and retry
    :args:
        conn:str - REST connection info
        total_rows:int - total number of rows inserted into AnyLog
        db_name:str - logical database name
    :params:
        status:bool
        row_count:int - number of rows inserted
    :return:
        difference between min/max value of insert_timestamp
    """
    status = False
    counter = 0
    conns = conn.split(',')
    conn_value = 0
    row_count = 0
    while status is False:
        row_count = __get_row_count(conn=conns[conn_value], db_name=db_name)
        if row_count >= total_rows or counter > 30: # wait about 15 minutes
            status = True
        else:
            time.sleep(30)
            counter += 1
        conn_value += 1
        if conn_value == len(conns):
            conn_value = 0

    return row_count, __insertion_time(conn=conn, db_name=db_name)


def print_summary(start_time:datetime.datetime, end_time:datetime.datetime, total_rows:int, anylog_rows_inserted:int,
                  processing_time:datetime.timedelta, anylog_insert_time:datetime.timedelta):
    """
    Print the summary data inserted
    :args:
        start_time:datetime.datetime - process start timestamp
        end_time:datetime.datetime - process end time
        total_rows:int - (expected) number of rows inserted
        anylog_rows_inserted:int - number of rows inserted
        processing_time:datetime.timedelta - amount of time insert process took (on REST side)
        anylog_insert_time:datetime.timedelta - amount of time it took AnyLog to insert the data
    :sample output:
        root@intel-operator1:~# cat ~/output.txt
        Overall Info:
            Start Time: 2022-08-21 22:16:26.657153
            End Time: 2022-08-21 22:43:18.148207
            Process Time: 0:26:51.491054
        Insert Process
            Expected Number of Rows: 10000000
            Number Rows of Inserted:10000000
            Generator Process Time: 0:04:49.098368
            AnyLog Processing Time: 0:26:37.546939
    """
    print(f'Overall Info:'
        +f'\n\tStart Time: {start_time}'
        +f'\n\tEnd Time: {end_time}'
        +f'\n\tProcess Time: {end_time - start_time}'
        +f'\nInsert Process:'
        +f'\n\tExpected Number of Rows: {total_rows}'
        +f'\n\tNumber Rows of Inserted:{anylog_rows_inserted}'
        +f'\n\tGenerator Process Time: {processing_time}'
        +f'\n\tAnyLog Processing Time: {anylog_insert_time}'
    )


def main():
    """
    The following provides the ability to insert data into AnyLog against logical table rand_data.
    :positional arguments:
      conn               REST connection info. If print then rows will be printed to screen
        - options: print, file, ip:port,ip:port,ip:port...
    :optional arguments:
      -h, --help         show this help message and exit
      --db-name DB_NAME  logical database name
      --rows ROWS        Number of row to insert
    :sample data:
        {"timestamp": "2022-08-23 00:48:36.219970", "value": 51.8812}
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default='print', help='REST connection info. If print then rows will be printed to screen')
    parser.add_argument('--db-name', type=str, default='test', help='logical database name')
    parser.add_argument('--table-name', type=str, default='rand_data', help='table to store data in')
    parser.add_argument('--total-rows', type=int, default=100000, help='Number of row to insert')
    args = parser.parse_args()

    if args.conn == 'print': # print rows to screen
        print_rows(total_rows=args.total_rows)
    elif args.conn == 'file': # store rows in {db_name}.rand_data.0.json file
        bkup_data(db_name=args.db_name, total_rows=args.total_rows)
    else: # send data to operator(s) via REST PUT
        start_time = datetime.datetime.now()
        processing_time, number_inserts = insert_data(conn=args.conn, total_rows=args.total_rows, db_name=args.db_name)
        anylog_rows_inserted, anylog_insert_time = insert_time(conn=args.conn, total_rows=args.total_rows, db_name=args.db_name)
        end_time = datetime.datetime.utcnow()

        print_summary(start_time=start_time, end_time=end_time, total_rows=args.total_rows,
                      anylog_rows_inserted=anylog_rows_inserted, processing_time=datetime.timedelta(seconds=processing_time),
                      anylog_insert_time=anylog_insert_time)

if __name__ == '__main__':
    main()

