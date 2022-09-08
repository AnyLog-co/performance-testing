import argparse
import requests

def get_ids(master_node:str)->list:
    """
    Get list of IDs for operator, cluster and table
    :args:
        master_node:str - Master node connection information
    :params:
        ids:list - list of ids
        headers:dict - REST header information
    :return:
        ids
    """
    ids = []
    headers = {
        'command': 'blockchain get (cluster, operator, table) bring [*][id] separator=,',
        'User-Agent': 'AnyLog/1.23'
    }

    try:
        r = requests.get(url=f'http://{master_node}', headers=headers)
    except Exception as error:
        print(f'Failed to execute GET against {master_node} (Error: {error})')
    else:
        if int(r.status_code) != 200:
            print(f'Failed to exeucte GET against {master_node} (Error: {r.status_code})')
        else:
            try:
                ids = r.text.split(',')
            except Exception as error:
                print(f'Failed to extract list of IDs (Error: {error})')

    return ids


def delete_policies(master_node:str, ids:list):
    """
    Drop policies from blockchain
    :args:
        master_node:str - Master Node IP + Port
        ids:list - list of Policy IDs to drop
    :params:
        r:requests.POST - results from request
    """
    for id in ids:
        headers = {
            'command': 'blockchain drop policy where id=%s' % id,
            'User-Agent': 'AnyLog/1.23'
        }

        try:
            r = requests.post(url=f'http://{master_node}', headers=headers)
        except Exception as error:
            print(f'Failed to remove policy with id {id} from {master_node} (Error: {error})')
        else:
            if int(r.status_code) != 200:
                print(f'Failed to remove policy with id {id} from {master_node} (Network Error: {r.status_code})')


def main():
    """
    Remove operator, cluster and table policies based on policy IDs
    :positional arguments:
        master_node     MASTER_NODE     master node REST IP + Port
    :params:
        ids:list - list of policy IDs
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('master_node', type=str, default='127.0.0.1:32049', help='master node REST IP + Port')
    args = parser.parse_args()

    ids = get_ids(master_node=args.master_node)
    delete_policies(master_node=args.master_node, ids=ids)


if __name__ == '__main__':
    main()