## Week 1 Homework

In this homework we'll prepare the environment 
and practice with terraform and SQL

## Question 1. Google Cloud SDK

Install Google Cloud SDK. What's the version you have? 

To get the version, run `gcloud --version`

>gcloud --version
```
Google Cloud SDK 369.0.0
alpha 2022.01.14
beta 2022.01.14
bq 2.0.72
core 2022.01.14
gsutil 5.6
```

## Google Cloud account 

Create an account in Google Cloud and create a project.


## Question 2. Terraform 

Now install terraform and go to the terraform directory (`week_1_basics_n_setup/1_terraform_gcp/terraform`)

After that, run

* `terraform init`
* `terraform plan`
* `terraform apply` 

Apply the plan and copy the output (after running `apply`) to the form.

It should be the entire output - from the moment you typed `terraform init` to the very end.

> terraform output
```
wtsang@CDYVRCWLT614:~/projects/dataeng-zc/week1_introduction/terraform$ terraform init

Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/google from the dependency lock file
- Using previously-installed hashicorp/google v4.7.0

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
wtsang@CDYVRCWLT614:~/projects/dataeng-zc/week1_introduction/terraform$ terraform plan
var.project
  Your GCP Project ID

  Enter a value: lateral-nomad-339206


Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "europe-west6"
      + project                    = "lateral-nomad-339206"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EUROPE-WEST6"
      + name                        = "dtc_data_lake_lateral-nomad-339206"
      + project                     = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_storage_class = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if
you run "terraform apply" now.
wtsang@CDYVRCWLT614:~/projects/dataeng-zc/week1_introduction/terraform$ terraform apply
var.project
  Your GCP Project ID

  Enter a value: lateral-nomad-339206


Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "europe-west6"
      + project                    = "lateral-nomad-339206"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EUROPE-WEST6"
      + name                        = "dtc_data_lake_lateral-nomad-339206"
      + project                     = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_storage_class = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=dtc_data_lake_lateral-nomad-339206]
google_bigquery_dataset.dataset: Creation complete after 3s [id=projects/lateral-nomad-339206/datasets/trips_data_all]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

## Prepare Postgres 

Run Postgres and load data as shown in the videos

We'll use the yellow taxi trips from January 2021:

```bash
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
```

You will also need the dataset with zones:

```bash 
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

Download this data and put it to Postgres

## Question 3. Count records 

How many taxi trips were there on January 15?

Consider only trips that started on January 15.

> SELECT COUNT(*) 
from yellow_taxi_data
where DATE(tpep_pickup_datetime) = '2021-01-15'
```
    count
0	53024

```

## Question 4. Largest tip for each day

Find the largest tip for each day. 
On which day it was the largest tip in January?

Use the pick up time for your calculations.

(note: it's not a typo, it's "tip", not "trip")

> SELECT 
    DATE(tpep_pickup_datetime) as day,
    max(tip_amount) as largest_tip
from yellow_taxi_data
group by 1
order by 1
```
	day	largest_tip
0	2008-12-31	0.00
1	2009-01-01	0.00
2	2020-12-31	4.08
3	2021-01-01	158.00
4	2021-01-02	109.15
5	2021-01-03	369.40
6	2021-01-04	696.48
7	2021-01-05	151.00
8	2021-01-06	100.00
9	2021-01-07	95.00
10	2021-01-08	100.00
11	2021-01-09	230.00
12	2021-01-10	91.00
13	2021-01-11	145.00
14	2021-01-12	192.61
15	2021-01-13	100.00
16	2021-01-14	95.00
17	2021-01-15	99.00
18	2021-01-16	100.00
19	2021-01-17	65.00
20	2021-01-18	90.00
21	2021-01-19	200.80
22	2021-01-20	1140.44
23	2021-01-21	166.00
24	2021-01-22	92.55
25	2021-01-23	100.00
26	2021-01-24	122.00
27	2021-01-25	100.16
28	2021-01-26	250.00
29	2021-01-27	100.00
30	2021-01-28	77.14
31	2021-01-29	75.00
32	2021-01-30	199.12
33	2021-01-31	108.50
34	2021-02-01	1.54
35	2021-02-22	1.76

```

> SELECT 
    DATE(tpep_pickup_datetime) as day,
    max(tip_amount) as largest_tip
from yellow_taxi_data
group by 1
order by 2 DESC
LIMIT 1
```
    day	        largest_tip
0	2021-01-20	1140.44

```

## Question 5. Most popular destination

What was the most popular destination for passengers picked up 
in central park on January 14?

Use the pick up time for your calculations.

Enter the zone name (not id). If the zone name is unknown (missing), write "Unknown" 

> SELECT 
    CASE WHEN zones."Zone" IS NULL
        THEN 'Unknown'
        ELSE zones."Zone" END as destination,
    yellow_taxi_data."DOLocationID" as destination_id,
    count(*) as num_trips
from yellow_taxi_data
LEFT JOIN zones
ON yellow_taxi_data."DOLocationID" = zones."LocationID"

where DATE(tpep_pickup_datetime) = '2021-01-14'
group by 1,2
ORDER by 3 DESC
LIMit 1
```

destination	destination_id	num_trips
0	Upper East Side North	236	6008

```

## Question 6. Most expensive locations

What's the pickup-dropoff pair with the largest 
average price for a ride (calculated based on `total_amount`)?

Enter two zone names separated by a slash

For example:

"Jamaica Bay / Clinton East"

If any of the zone names are unknown (missing), write "Unknown". For example, "Unknown / Clinton East". 


> SELECT 
    "PULocationID",
    "DOLocationID",
    CONCAT(COALESCE(zpu."Zone",'Unknown'),'/',COALESCE(zdo."Zone",'Unknown')) as route,
    AVG(total_amount) as average_price
from yellow_taxi_data
LEFT JOIN zones zdo
ON yellow_taxi_data."DOLocationID" = zdo."LocationID"
LEFT JOIN zones zpu
ON yellow_taxi_data."PULocationID" = zpu."LocationID"
group by 1,2,3
ORDER by 4 DESC
LIMIT 1
```

	PULocationID	DOLocationID	route	average_price
0	4	265	Alphabet City/Unknown	2292.4

```

## Submitting the solutions

* Form for submitting: https://forms.gle/yGQrkgRdVbiFs8Vd7
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 24 January, 17:00 CET

