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
### Query 
### Operator

## Inserting Data 

## Executing Queries
The _Query_ node also deploys the Remote-CLI, which you can use instead of using cURL. Directions for Remote-CLI can be  
found [here](https://github.com/AnyLog-co/documentation/blob/master/northbound%20connectors/remote_cli.md). Please make 
sure the logical database and table names are consistent with your deployment.   

* Scans the data to determine min, max, count over the data.
```shell
curl -X GET ${QUERY_NODE_IP}:${QUERY_NODE_PORT} \
  -H 'command: sql test format=table and extend=(+ip, +node_name) "select min(insert_timestamp), max(insert_timestamp), count(*)::format(:,) from rand_data_small_6_25m;"' \ 
  -H 'User-Agent: AnyLog/1.23' \
  -H 'destination Network' 
```

* Is doing more CPU intensive - returning the summary of every hour
```shell
curl -X GET ${QUERY_NODE_IP}:${QUERY_NODE_PORT} \
  -H 'command: sql test format=table  "select increments(hour, 1, timestamp), min(timestamp), max(timestamp), min(value), avg(value), max(value), count(*)::format(:,) from rand_data_small_6_50m;"' \ 
  -H 'User-Agent: AnyLog/1.23' \ 
  -H 'destination Network' 
```
