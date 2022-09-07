# Performance Testing 

The following repository provides the tools needed to test AnyLog performance. 


## Requirements
* 2 machines - either VM or physical to host _Master_ and _Query_ nodes 
* 2 or more machines (either VM or physical) to act the _Operator_ nodes   
* All nodes should be able to communicate with one another

## Testing Process 
1. Deploy _Master_ + _Query_ Nodes 
2. Deploy 1 _Operator_ node  
3. Load data into _Operator_ node
4. Execute queries against the operator 
5. Clean the data on the operator node + remove node information from master 
6. Deploy 2 _Operator_ nodes 
7. Load half (1/2) of the data into Operator A and Operator B 
8. Execute queries against both the operator nodes 
9. Repeat Steps 5-8 with incrementing number of _Operator_ nodes  

At the end of step 8, you should notice that the queries run faster when data is distributed on 2 nodes, as opposed to 1.   

## Deploying Nodes
### Master
1. docker login into AnyLog
```shell
docker login -u anyloguser -p ${DOCKER_LOGIN}
``` 

2. clone [performance-testing](https://github.com/AnyLog-co/performance-testing) into all your nodes
```shell
git clone https://github.com/AnyLog-co/performance-testing
```

3. (Optional) In [docker-compose](deployments/anylog-master/anylog_configs.env) update configurations like: 
    * Node Name
    * Company Name 
    * AnyLog TCP or REST ports - note if you change the TCP port, you need to update the _LEDGER_CONN_ accordingly 
    * Blockchain sync time
   

4. Deploy node - this will also deploy Postgres
```shell
cd performance-testing/deployments/anylog-master
docker-compose up -d 
```

5. Using cURL get connection information  - You'll be using the external TCP information as the `LEDGER_CONN` if other 
nodes are on a different network, and the local TCP information as the `LEDGER_CONN` if they're on the same network.
```shell
curl -X GET ${MASTER_NODE_IP}:${MASTER_NODE_PORT} \ 
  -H "command: get connections" \ 
  -H "User-Agent: AnyLog/1.23"
  
<< COMMENT
# Sample Output
Type      External Address    Local Address       
---------|-------------------|-------------------|
TCP      |23.239.12.151:32348|192.168.0.131:32348|
REST     |23.239.12.151:32349|192.168.0.131:32349|
Messaging|Not declared       |Not declared       | 
<< 
```

### Query 
1. docker login into AnyLog
```shell
docker login -u anyloguser -p ${DOCKER_LOGIN}
``` 

2. clone [performance-testing](https://github.com/AnyLog-co/performance-testing) into all your nodes
```shell
git clone https://github.com/AnyLog-co/performance-testing
```

3. In [docker-compose](deployments/query-remote-cli/anylog_configs.env) update `LEDGER_CONN` information, with the TCP 
connection found in step 5 of the Master node. Remember, you'll be using the external TCP information as the `LEDGER_CONN` 
if other nodes are on a different network, and the local TCP information as the `LEDGER_CONN` if they're on the same network.


4. (Optional) In [docker-compose](deployments/query-remote-cli/anylog_configs.env) update configurations like: 
    * Node Name
    * Company Name 
    * AnyLog TCP or REST ports - note if you change the TCP port, you need to update the _LEDGER_CONN_ accordingly 
    * Blockchain sync time
    * Query poool
   

5. Deploy node - this will also deploy Postgres
```shell
cd performance-testing/deployments/query-remote-cli
docker-compose up -d 
```

### Operator
The [deployments](deployments) directory has 4 operator nodes that are identical to one another, with exception to their 
name and cluster. In order to deploy 1 or more operator nodes on the same machine, you need to change replace 
"anylog-operator-node" with something else in the coressponding docker-compose file. 

1. docker login into AnyLog
```shell
docker login -u anyloguser -p ${DOCKER_LOGIN}
``` 

2. clone [performance-testing](https://github.com/AnyLog-co/performance-testing) into all your nodes
```shell
git clone https://github.com/AnyLog-co/performance-testing
```
 
3. In [docker-compose](deployments/anylog-operator1/anylog_configs.env) update `LEDGER_CONN` information, with the TCP 
connection found in step 5 of the Master node. Remember, you'll be using the external TCP information as the `LEDGER_CONN` 
if other nodes are on a different network, and the local TCP information as the `LEDGER_CONN` if they're on the same network.


4. (Optional) In [docker-compose](deployments/anylog-operator1/anylog_configs.env) update configurations like: 
    * Node Name
    * Company Name 
    * AnyLog TCP or REST ports - note if you change the TCP port, you need to update the _LEDGER_CONN_ accordingly 
    * logical database name
    * cluster name - please note if 2 or more operators have the same cluster then the data between them will be shared (ie. High-Availability) 
    * Blockchain sync time
    * Operator threads 
    * Query pool
    
5. Deploy node - this will also deploy Postgres
```shell
cd performance-testing/deployments/anylog-operator1
docker-compose up -d 
```

### Updating Query Pool 
The `QUERY_POOL` value is used to set the number of threads supporting queries (the default is 3). To change / update 
on an operator or query node execute the following: 
1. Attach to the node
```shell
# view all docker instances  
docker ps -a 

# attach to a docker instance
docker attach --detach-keys=ctrl-d ${DOCKER_SERVICE_NAME}

<< COMMENT
# Sample Output - list of docker services on an operator node
CONTAINER ID   IMAGE                                COMMAND                  CREATED        STATUS        PORTS                                           NAMES
3bfc357af701   anylogco/anylog-network:predevelop   "/bin/sh -c 'python3…"   17 hours ago   Up 17 hours                                                   anylog-operator-node
7273d336e561   postgres:14.0-alpine                 "docker-entrypoint.s…"   43 hours ago   Up 17 hours   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp       postgres

# Sample command for anylog-operator-node
docker attach --detach-keys=ctrl-d anylog-operator-node
<< 
```
2. exit workers 
```anylog
al > exit workers 
```
3. set query pool to a new value
```anylog
al> set query pool 6 
```

### Clean node
1. On Master node execute [clean_node.py](clean_node.py) - remove policies from blockchain 
```shell
python3 performance-testing/clean_node.py ${MASTER_NODE_IP}:${MASTER_NODE_REST}
```

2. On Operator node - remove all data 
```shell
cd performance-testing/deployments/anylog-operator1
docker-compose down -v 
```

## Inserting Data 
The following inserts  data using the REST _PUT_ command into an Operator node; data is over a 24-hour period, and 
consists of only timestamp and value.  

```shell
python3 performance-testing/data_generator.py ${OPERATOR_NODE_IP}:${OPERATOR_NODE_REST_PORT} \
  --db-name test \ 
  --table-name  rand_data_small_6_25m \
  --total-rows 25000000 \ 
```

Once [data_generator.py](data_generator.py) is complete, the Operator node may not have finished inserting all the data 
into the database. To check the status of the data there are 3 things you can do:

* get streaming - Statistics on the streaming processes.
```shell
curl -X GET ${OPERATOR_NODE_IP}:${OPERATOR_NODE_REST_PORT} \
   -H "command: get streaming" \ 
   -H "User-Agent: AnyLog/1.23" 
```
* get operator - Information on the Operator processes and configuration.
```shell
curl -X GET ${OPERATOR_NODE_IP}:${OPERATOR_NODE_REST_PORT} \
   -H "command: get operator" \ 
   -H "User-Agent: AnyLog/1.23" 
```

* query the data - notice the destination is set **not** `network` as we want information only about a specific operator.
```shell
curl -X GET ${OPERATOR_NODE_IP}:${OPERATOR_NODE_REST_PORT} \
   -H 'command: sql test format=table "select count(*) from rand_data_small_6_25m' \ 
   -H "User-Agent: AnyLog/1.23" \ 
   -H "destination: ${OPERATOR_NODE_IP}:${OPERATOR_NODE_TCP_PORT}" 
```

## Executing Queries
The _Query_ node also deploys the Remote-CLI, which you can use instead of using cURL. Directions for Remote-CLI can be found [here](https://github.com/AnyLog-co/documentation/blob/master/northbound%20connectors/remote_cli.md). Please make sure the logical database and table names are consistent with your deployment.   

* Scans the data to determine min, max, count over the data.
```shell
curl -X GET ${QUERY_NODE_IP}:${QUERY_NODE_REST_PORT} \
  -H 'command: sql test format=table and extend=(+ip, +node_name) "select min(insert_timestamp), max(insert_timestamp), count(*)::format(:,) from rand_data_small_6_25m;"' \ 
  -H 'User-Agent: AnyLog/1.23' \
  -H 'destination Network' 
```

* Is doing more CPU intensive - returning the summary of every hour
```shell
curl -X GET ${QUERY_NODE_IP}:${QUERY_NODE_REST_PORT} \
  -H 'command: sql test format=table  "select increments(hour, 1, timestamp), min(timestamp), max(timestamp), min(value), avg(value), max(value), count(*)::format(:,) from rand_data_small_6_25m;"' \ 
  -H 'User-Agent: AnyLog/1.23' \ 
  -H 'destination Network' 
```
