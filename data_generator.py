import argparse
import datetime
import json
import math
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

# base timestamp 2022-08-27 15:50:12
START_TIMESTAMP = datetime.datetime(year=2022, month=8, day=27, hour=15, minute=50, second=12) + datetime.timedelta(microseconds=random.choice(range(100, 300000)))
SECOND_INCREMENTS = 0.864
ROWS_24h_INCREMENTS = 100000


VALUE_ARRAY = [
    -1.2246467991473532e-16, -1.0, 1.2246467991473532e-16, -1.0, 6.123233995736766e-17, -1.633123935319537e+16,
    -0.8660254037844386, 0.5000000000000001, -1.7320508075688767, -0.8414709848078965, 0.5403023058681398,
    -1.557407724654902, -0.7071067811865475, 0.7071067811865476, -0.9999999999999999, -0.49999999999999994,
    0.8660254037844387, -0.5773502691896256, -0.3826834323650898, 0.9238795325112867, -0.4142135623730951, 0.0, 1.0,
    0.0, 0.3826834323650898, 0.9238795325112867, 0.4142135623730951, 0.49999999999999994, 0.8660254037844387,
    0.5773502691896256, 0.7071067811865475, 0.7071067811865476, 0.9999999999999999, 0.8414709848078965,
    0.5403023058681398, 1.557407724654902, 0.8660254037844386, 0.5000000000000001, 1.7320508075688767, 1.0,
    6.123233995736766e-17, 1.633123935319537e+16, 1.2246467991473532e-16, -1.0, -1.2246467991473532e-16,
    1.2246467991473532e-16, -1.0, -1.2246467991473532e-16, 1.0, 6.123233995736766e-17, 1.633123935319537e+16,
    0.8660254037844386, 0.5000000000000001, 1.7320508075688767, 0.8414709848078965, 0.5403023058681398,
    1.557407724654902, 0.7071067811865475, 0.7071067811865476, 0.9999999999999999, 0.49999999999999994,
    0.8660254037844387, 0.5773502691896256, 0.3826834323650898, 0.9238795325112867, 0.4142135623730951,
    0.0, 1.0, 0.0, -0.3826834323650898, 0.9238795325112867, -0.4142135623730951, -0.49999999999999994,
    0.8660254037844387, -0.5773502691896256, -0.7071067811865475, 0.7071067811865476, -0.9999999999999999,
    -0.8414709848078965, 0.5403023058681398, -1.557407724654902, -0.8660254037844386, 0.5000000000000001,
    -1.7320508075688767, -1.0, 6.123233995736766e-17, -1.633123935319537e+16, -1.2246467991473532e-16, -1.0,
    1.2246467991473532e-16
]


def __send_data(conn:str, db_name:str, table_name:str, payload:list, send_time:float)->(bool, float):
    """
    Send data via REST PUT
    :args:
        conn:str - REST connection information
        db_name:str - logical database name
        table_name:str - logical table name
        payload:list - content to be sent into AnyLog
        send_time:float - total process time thus far
    :params:
        status:bool
        header:dict - REST header information
        payloads:str - JSON list of payload
        r:requests.Requests - POST request results
    :return:
        status, updated send_time
    """
    status = True
    header = {
        'type': 'json',
        'dbms': db_name,
        'table': table_name,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    try:
        payloads = json.dumps(payload)
    except Exception as error:
        print(f'Failed to convert payload to dict (Error: {error})')
        status = False
    else:
        start = time.time()
        try:
            r = requests.put(url=f'http://{conn}', headers=header, data=payloads)
        except Exception as error:
            print(f'Failed to PUT data into {conn} (Error: {error})')
            status = False
        else:
            send_time += time.time() - start
            if int(r.status_code) != 200:
                print(f'Failed to PUT data int {conn} (Network Error: {r.status_code})')
                status = False

    return status, send_time


def __generate_row(value:float, base_row_time:float, row_counter:int)->dict:
    """
    Generate row to be inserted
    :global:
        START_TIMESTAMP:datetime.datetime - intial timestamp
        SECOND_INCREMENTS:float - Based on ROWS_24h_INCREMENTS, calculate increments for 24 hour period
        ROWS_24h_INCREMENTS:int - based number of rows in 24 hours
    :args:
        value:float - pi value for VALUE_ARRAY
        total_rows:int - total number of row to insert
        row_counter:int - current row to insert
    :params:
        row_value:float - trig calculation based on value
            - if row_counter % 10 - use tangent
            - if row_counter % 2 - use sine
            - else - use cosine
        seconds:float - increments size
        now:datetime.datetime - row timestamp
        row:dict - {timestamp, value} object to store in operator
    :return:
        row
    """
    # if row_counter % 10 == 0:
    #     row_value = math.tan(value)
    # elif row_counter % 2 == 0:
    #     row_value = math.sin(value)
    # else:
    #     row_value = math.cos(value)
    seconds = base_row_time * row_counter
    timestamp = START_TIMESTAMP + datetime.timedelta(seconds=seconds)
    row = {'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'), 'value': value}

    return row


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
    value_array = 0
    total_time = 0
    values = []
    send_time = 0
    row_times = 0

    base_row_time = SECOND_INCREMENTS * (ROWS_24h_INCREMENTS / args.total_rows)

    for row_counter in range(args.total_rows):

        values.append(__generate_row(value=VALUE_ARRAY[value_array], base_row_time=base_row_time, row_counter=row_counter))
        value_array += 1
        if value_array == len(VALUE_ARRAY):
            value_array = 0

        if len(values) >= 10000:
            status, updated_send_time = __send_data(conn=args.conn, db_name=args.db_name, table_name=args.table_name,
                                                    payload=values, send_time=send_time)
            if status is True:
                values = []
                send_time = updated_send_time

    if len(values) > 0:
        status, updated_send_time = __send_data(conn=args.conn, db_name=args.db_name, table_name=args.table_name,
                                                payload=values, send_time=send_time)
        if status is True:
            send_time = updated_send_time

    print(f'Insert Time: {datetime.timedelta(seconds=send_time)}')


if __name__ == '__main__':
    main()

