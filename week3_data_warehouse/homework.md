## Homework
[Form](https://forms.gle/ytzVYUh2RptgkvF79)  
We will use all the knowledge learned in this week. Please answer your questions via form above.  
**Deadline** for the homework is 14th Feb 2022 17:00 CET.



### Question 1: 
**What is count for fhv vehicles data for year 2019**  
Can load the data for cloud storage and run a count(*)

> Query:
```sql
SELECT COUNT(*) FROM `lateral-nomad-339206.trips_data_all.fhv_tripdata` 
WHERE EXTRACT(YEAR FROM DATE(pickup_datetime)) = 2019
```

> Result:
```
42084899
```

### Question 2: 
**How many distinct dispatching_base_num we have in fhv for 2019**  
Can run a distinct query on the table from question 1

> Query:
```sql
SELECT COUNT(DISTINCT dispatching_base_num ) FROM `lateral-nomad-339206.trips_data_all.fhv_tripdata` 
WHERE EXTRACT(YEAR FROM DATE(pickup_datetime)) = 2019
```

> Result:
```
792
```

### Question 3: 
**Best strategy to optimise if query always filter by dropoff_datetime and order by dispatching_base_num**  
Review partitioning and clustering video.   
We need to think what will be the most optimal strategy to improve query 
performance and reduce cost.

> Answer:
```
Partition by dropoff_datetime because that is a time unit column
Cluster by dispatching_base_num as that will optimize sorting and it is a string
```

### Question 4: 
**What is the count, estimated and actual data processed for query which counts trip between 2019/01/01 and 2019/03/31 for dispatching_base_num B00987, B02060, B02279**  
Create a table with optimized clustering and partitioning, and run a 
count(*). Estimated data processed can be found in top right corner and
actual data processed can be found after the query is executed.

> Query:
```sql
CREATE OR REPLACE TABLE `lateral-nomad-339206.trips_data_all.fhv_tripdata_partitioned`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY dispatching_base_num AS
SELECT * FROM `lateral-nomad-339206.trips_data_all.fhv_tripdata`;

SELECT COUNT(*) FROM `lateral-nomad-339206.trips_data_all.fhv_tripdata_partitioned`
WHERE DATE(pickup_datetime) BETWEEN  '2019-01-01' AND '2019-03-31'
AND dispatching_base_num IN ('B00987', 'B02060', 'B02279');
```

> Result:
```
Count: 26647
Estimated: 400.1 MiB
Actual: 154.25 MB
```

### Question 5: 
**What will be the best partitioning or clustering strategy when filtering on dispatching_base_num and SR_Flag**  
Review partitioning and clustering video. 
Partitioning cannot be created on all data types.

> Answer:
```
Partition by SR_FLAG because its an int
Cluster by dispatching_base_num because that is a string
```


### Question 6: 
**What improvements can be seen by partitioning and clustering for data size less than 1 GB**  
Partitioning and clustering also creates extra metadata.  
Before query execution this metadata needs to be processed.

No significant improvement for less than 1 GB and potentially worse performance due to metadata

### (Not required) Question 7: 
**In which format does BigQuery save data**  
Review big query internals video.

Bigquery is a columnar store